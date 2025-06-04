from flask import Flask, request, render_template, session, jsonify, flash, redirect, url_for
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import io
import base64

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def dataframe_to_dict(df):
    """Convert DataFrame to a serializable format for session storage"""
    return {
        'data': df.to_dict('records'),
        'columns': list(df.columns),
        'index': list(df.index)
    }

def dict_to_dataframe(df_dict):
    """Convert serialized DataFrame back to pandas DataFrame"""
    if df_dict is None:
        return None
    df = pd.DataFrame(df_dict['data'])
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        file1 = request.files.get('file1')
        file2 = request.files.get('file2')
        
        if not file1 or not file2:
            flash('Please upload both files', 'error')
            return redirect(url_for('index'))
        
        # Read first file
        if file1.filename.endswith(('.xlsx', '.xls')):
            df1 = pd.read_excel(file1)
        elif file1.filename.endswith('.csv'):
            df1 = pd.read_csv(file1)
        else:
            flash('File 1 must be CSV or Excel format', 'error')
            return redirect(url_for('index'))
        
        # Read second file
        if file2.filename.endswith(('.xlsx', '.xls')):
            df2 = pd.read_excel(file2)
        elif file2.filename.endswith('.csv'):
            df2 = pd.read_csv(file2)
        else:
            flash('File 2 must be CSV or Excel format', 'error')
            return redirect(url_for('index'))
        
        # Store DataFrames in session
        session['df1'] = dataframe_to_dict(df1)
        session['df2'] = dataframe_to_dict(df2)
        session['df1_name'] = file1.filename
        session['df2_name'] = file2.filename
        
        flash(f'Successfully uploaded {file1.filename} ({len(df1)} rows) and {file2.filename} ({len(df2)} rows)', 'success')
        
        return render_template('uploaded.html', 
                             df1_info={'name': file1.filename, 'shape': df1.shape, 'columns': list(df1.columns)},
                             df2_info={'name': file2.filename, 'shape': df2.shape, 'columns': list(df2.columns)})
        
    except Exception as e:
        flash(f'Error uploading files: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/command', methods=['POST'])
def process_command():
    try:
        command = request.form.get('command', '').strip()
        if not command:
            flash('Please enter a command', 'error')
            return redirect(url_for('index'))
        
        # Check if files are uploaded
        if 'df1' not in session or 'df2' not in session:
            flash('Please upload files first', 'error')
            return redirect(url_for('index'))
        
        # Interpret the command
        cmd = interpret_command(command)
        
        if cmd['action'] == 'join':
            result = perform_join(cmd)
            if result['success']:
                flash('Tables joined successfully!', 'success')
                return render_template('joined.html', 
                                     join_info=result['info'],
                                     sample_data=result['sample_data'])
            else:
                flash(f'Error joining tables: {result["error"]}', 'error')
                return redirect(url_for('index'))
                
        elif cmd['action'] == 'chart':
            result = generate_chart(cmd)
            if result['success']:
                return render_template('result.html', 
                                     chart=result['chart'],
                                     chart_info=result['info'])
            else:
                flash(f'Error creating chart: {result["error"]}', 'error')
                return redirect(url_for('index'))
        else:
            flash('Command not recognized. Try "join tables on column_name" or "create bar chart of column1 by column2"', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'Error processing command: {str(e)}', 'error')
        return redirect(url_for('index'))

def interpret_command(command):
    """Use OpenAI to interpret natural language commands"""
    system_prompt = """You are an assistant that interprets commands for data processing and visualization.

For join commands, return JSON like:
{"action": "join", "parameters": {"type": "inner", "key": "column_name"}}

Supported join types: "inner", "left", "right", "outer"

For visualization commands, return JSON like:
{"action": "chart", "parameters": {"type": "bar", "x": "column_name", "y": "column_name", "aggregation": "sum"}}

Supported chart types: "bar", "line", "scatter", "pie", "histogram"
Supported aggregations: "sum", "mean", "count", "max", "min"

Examples:
- "Join tables on CustomerID" -> {"action": "join", "parameters": {"type": "inner", "key": "CustomerID"}}
- "Left join on user_id" -> {"action": "join", "parameters": {"type": "left", "key": "user_id"}}
- "Create bar chart of sales by region" -> {"action": "chart", "parameters": {"type": "bar", "x": "region", "y": "sales", "aggregation": "sum"}}
- "Show line chart of revenue over time" -> {"action": "chart", "parameters": {"type": "line", "x": "time", "y": "revenue"}}

Always return valid JSON only, no additional text."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": command}
            ],
            temperature=0
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"Error interpreting command: {e}")
        return {"action": "error", "message": str(e)}

def perform_join(cmd):
    """Perform table join based on command parameters"""
    try:
        df1 = dict_to_dataframe(session['df1'])
        df2 = dict_to_dataframe(session['df2'])
        
        join_type = cmd['parameters'].get('type', 'inner')
        key = cmd['parameters']['key']
        
        # Check if key exists in both DataFrames
        if key not in df1.columns:
            return {"success": False, "error": f"Column '{key}' not found in {session['df1_name']}"}
        if key not in df2.columns:
            return {"success": False, "error": f"Column '{key}' not found in {session['df2_name']}"}
        
        # Perform the join
        joined_df = df1.merge(df2, how=join_type, on=key, suffixes=('_table1', '_table2'))
        
        # Store joined data in session
        session['joined_data'] = dataframe_to_dict(joined_df)
        
        # Get sample data for display
        sample_data = joined_df.head(10).to_dict('records')
        
        join_info = {
            'type': join_type,
            'key': key,
            'shape': joined_df.shape,
            'columns': list(joined_df.columns)
        }
        
        return {
            "success": True, 
            "info": join_info,
            "sample_data": sample_data
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def generate_chart(cmd):
    """Generate visualization based on command parameters"""
    try:
        # Use joined data if available, otherwise use first table
        if 'joined_data' in session:
            data = dict_to_dataframe(session['joined_data'])
            data_source = "joined data"
        else:
            data = dict_to_dataframe(session['df1'])
            data_source = session['df1_name']
        
        chart_type = cmd['parameters']['type']
        x = cmd['parameters']['x']
        y = cmd['parameters'].get('y')
        agg = cmd['parameters'].get('aggregation')
        
        # Check if columns exist
        if x not in data.columns:
            return {"success": False, "error": f"Column '{x}' not found in data"}
        if y and y not in data.columns:
            return {"success": False, "error": f"Column '{y}' not found in data"}
        
        # Apply aggregation if specified
        if agg and y:
            if agg == 'count':
                plot_data = data.groupby(x).size().reset_index(name='count')
                y = 'count'
            else:
                plot_data = data.groupby(x)[y].agg(agg).reset_index()
        else:
            plot_data = data
        
        # Create the chart
        if chart_type == 'bar':
            fig = px.bar(plot_data, x=x, y=y, title=f'Bar Chart: {y} by {x}')
        elif chart_type == 'line':
            fig = px.line(plot_data, x=x, y=y, title=f'Line Chart: {y} over {x}')
        elif chart_type == 'scatter':
            fig = px.scatter(plot_data, x=x, y=y, title=f'Scatter Plot: {y} vs {x}')
        elif chart_type == 'pie':
            fig = px.pie(plot_data, names=x, values=y, title=f'Pie Chart: {y} by {x}')
        elif chart_type == 'histogram':
            fig = px.histogram(plot_data, x=x, title=f'Histogram: Distribution of {x}')
        else:
            return {"success": False, "error": f"Unsupported chart type: {chart_type}"}
        
        # Style the chart
        fig.update_layout(
            width=800,
            height=500,
            font=dict(size=12),
            title_x=0.5
        )
        
        chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        chart_info = {
            'type': chart_type,
            'x': x,
            'y': y,
            'aggregation': agg,
            'data_source': data_source,
            'data_shape': plot_data.shape
        }
        
        return {
            "success": True,
            "chart": chart_html,
            "info": chart_info
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route('/reset')
def reset_session():
    """Clear all session data"""
    session.clear()
    flash('Session reset successfully', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 