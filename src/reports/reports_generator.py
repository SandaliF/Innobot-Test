import pandas as pd
import mysql.connector

class ReportGenerator:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def generate_report(self):
        query = """
        SELECT 
            COUNT(*) AS total_products,
            AVG(price) AS average_price,
            SUM(CASE WHEN availability = 'Out of Stock' THEN 1 ELSE 0 END) AS out_of_stock
        FROM ads;
        """
        report_data = pd.read_sql(query, self.connection)
        return report_data

    def save_report(self, report_data, file_path):
        report_data.to_csv(file_path, index=False)  # Save as CSV
        # Uncomment below to save as HTML
        # report_data.to_html(file_path.replace('.csv', '.html'), index=False)

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    report_gen = ReportGenerator(
        host="localhost",
        user="root",    
        password="innobot", 
        database="ad_data"   
    )
    
    report = report_gen.generate_report()
    print(report)  # Print the report to console
    report_gen.save_report(report, "C:/Users/Administrator/Documents/Sandali Fernando/src/reports/report.csv")
    report_gen.close()
