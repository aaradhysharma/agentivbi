# agentivBI - Automated Business Intelligence

**agentivBI** is a Python web application that automates business intelligence tasks using natural language processing. Upload CSV or Excel files, describe your data operations in plain English, and get instant visualizations - no manual steps required!

![agentivBI Demo](https://img.shields.io/badge/Status-Ready%20to%20Use-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-red)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-orange)

## 🚀 Features

- **Natural Language Processing**: Describe data operations in plain English
- **Automated Table Joins**: Support for inner, left, right, and outer joins
- **Interactive Visualizations**: Generate bar charts, line charts, pie charts, scatter plots, and histograms
- **File Support**: Upload CSV and Excel files (.csv, .xlsx, .xls)
- **Modern UI**: Beautiful, responsive web interface with Bootstrap
- **Real-time Processing**: Instant results with session-based state management
- **Export Options**: Save charts as images or interact with Plotly controls

## 🏗️ Architecture

- **Frontend**: Flask-based web interface with Bootstrap styling
- **NLP Engine**: OpenAI GPT-3.5-turbo for command interpretation
- **Data Processing**: Pandas for table operations and joins
- **Visualization**: Plotly for interactive charts
- **State Management**: Flask sessions for data persistence

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Modern web browser

## 🛠️ Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd agentivbi
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root (copy from `env_template.txt`):
   ```bash
   cp env_template.txt .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SECRET_KEY=your_secret_key_for_sessions_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎯 How to Use

### Step 1: Upload Your Data
- Upload two CSV or Excel files using the web interface
- View file information and available columns

### Step 2: Join Tables (Optional)
Use natural language to describe how to join your tables:
```
- "Join tables on CustomerID with inner join"
- "Left join on user_id"
- "Merge tables on product_id with outer join"
```

### Step 3: Create Visualizations
Describe the chart you want to create:
```
- "Create bar chart of sales by region"
- "Show line chart of revenue over month"
- "Make pie chart of count by category"
- "Generate scatter plot of price vs quantity"
- "Create histogram of age distribution"
```

## 💡 Example Commands

### Join Operations
```
✅ "Join tables on ID with inner join"
✅ "Left join on customer_id"
✅ "Merge data on product_code with outer join"
✅ "Right join tables on order_id"
```

### Visualizations
```
✅ "Create bar chart of sales by region"
✅ "Show line chart of revenue over time"
✅ "Make pie chart of count by category"
✅ "Generate scatter plot of price vs quantity"
✅ "Create histogram of age"
✅ "Bar chart showing sum of amount by department"
✅ "Line chart of average score over month"
```

## 🎨 Supported Chart Types

| Chart Type | Use Case | Example Command |
|------------|----------|-----------------|
| **Bar Chart** | Compare categories | "Create bar chart of sales by region" |
| **Line Chart** | Show trends over time | "Show line chart of revenue over month" |
| **Pie Chart** | Show proportions | "Make pie chart of count by category" |
| **Scatter Plot** | Show relationships | "Generate scatter plot of price vs quantity" |
| **Histogram** | Show distributions | "Create histogram of age" |

## 🔧 Supported Aggregations

- **Sum**: Total values
- **Mean**: Average values
- **Count**: Number of records
- **Max**: Maximum values
- **Min**: Minimum values

## 📁 Project Structure

```
agentivbi/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── env_template.txt      # Environment variables template
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with styling
│   ├── index.html        # Landing page
│   ├── uploaded.html     # File upload confirmation
│   ├── joined.html       # Join results display
│   └── result.html       # Visualization display
└── test                  # Test file (can be removed)
```

## 🛡️ Security Considerations

- **API Keys**: Store OpenAI API key in environment variables, never in code
- **Secret Key**: Use a strong, unique secret key for Flask sessions
- **File Uploads**: Only CSV and Excel files are accepted
- **Session Data**: Data is stored in memory and cleared on session reset

## 🚀 Deployment Options

### Local Development
```bash
python app.py
```

### Production Deployment
For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up a reverse proxy (Nginx)
- Using environment variables for configuration
- Implementing proper logging and monitoring

### Cloud Deployment
Deploy easily on platforms like:
- **Heroku**: Web-based deployment
- **Render**: Modern hosting platform
- **Railway**: Simple deployment
- **DigitalOcean App Platform**: Managed hosting

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your API key is correctly set in the `.env` file
   - Check that you have sufficient API credits

2. **File Upload Issues**
   - Verify file format (CSV, Excel)
   - Check file size (large files may cause memory issues)

3. **Join Errors**
   - Ensure the join column exists in both tables
   - Check for exact column name matches (case-sensitive)

4. **Chart Generation Errors**
   - Verify column names exist in your data
   - Ensure numeric columns for aggregations

### Getting Help

If you encounter issues:
1. Check the browser console for JavaScript errors
2. Review the Flask application logs
3. Verify your data file formats and column names
4. Ensure your OpenAI API key is valid and has credits

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional chart types
- Advanced data transformations
- Enhanced error handling
- Performance optimizations
- UI/UX improvements

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- OpenAI for GPT-3.5-turbo
- Plotly for interactive visualizations
- Pandas for data manipulation
- Flask for web framework
- Bootstrap for UI components

---

**Happy Analyzing!** 🎉

Get started by uploading your data files and describing what you want to do in plain English. agentivBI will handle the rest! 