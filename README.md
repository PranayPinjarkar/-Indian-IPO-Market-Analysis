# 📈 Indian IPO Analysis Dashboard

A dynamic and interactive data visualization dashboard built with **Streamlit** to analyze the Indian IPO market. This application allows investors and analysts to explore historical IPO data, understand market trends, and drill down into individual company performance.

## 🚀 Key Features

*   **📊 Market Snapshot**: Get a quick overview of the market with high-level KPIs like Total IPOs, Average Listing Gains, and Success Rates.
*   **📉 Distribution Analysis**: Visualize the spread of Listing Gains, Issue Sizes, and Subscription numbers using interactive histograms.
*   **🔍 Variable Relationships**: Explore correlations between different metrics (e.g., *Does a larger Issue Size lead to lower Gains?*) using customizable scatter plots.
*   **🏢 Company Explorer**: deep-dive into specific companies to view:
    *   **Scorecard**: Key stats like Issue Price, Size, and Gains.
    *   **Subscription Breakdown**: Understand institutional (QIB) vs. retail (RII) interest.
    *   **Market Comparison**: See how a company compares to the overall market average.
*   **🗓️ Temporal Filtering**: Filter data by specific years to analyze market cycles.

## 🛠️ Tech Stack

*   **Python**: Core programming language.
*   **Streamlit**: For building the web application UI.
*   **Pandas**: For data manipulation and analysis.
*   **Plotly Express**: For creating interactive and responsive charts.

## ⚙️ Installation & Setup

Follow these steps to get the project running on your local machine.

### Prerequisites
*   Python 3.8 or higher installed.

### Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/PranayPinjarkar/Indian_IPO_analysis.git
    cd Indian_IPO_analysis
    ```

2.  **Install Dependencies**
    It's recommended to create a virtual environment first.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

4.  **Open in Browser**
    The app should automatically open in your default browser at `http://localhost:8501`.

## 📂 Project Structure

```
indian-ipo-analysis/
├── app.py                      # Main Streamlit application source code
├── Indian_IPO_Market_Data.csv  # Dataset file (Ensure this is present)
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## 🤝 Contributing

Contributions are welcome! If you have suggestions or bug reports, please open an issue or submit a pull request.

---
*Built with ❤️ for Financial Analysts and Data Enthusiasts.*
