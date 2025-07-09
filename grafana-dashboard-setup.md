# Grafana Dashboard Setup Guide

## Step 1: Access Grafana
1. Open your browser and go to: http://localhost:3001
2. Login with:
   - Username: `admin`
   - Password: `admin123`

## Step 2: Add Prometheus Data Source
1. Go to **Configuration** (gear icon) → **Data Sources**
2. Click **"Add data source"**
3. Select **"Prometheus"**
4. Set the URL to: `http://prometheus-service:9090`
5. Click **"Save & Test"**

## Step 3: Create New Dashboard
1. Click the **"+"** icon in the left sidebar
2. Select **"Dashboard"**
3. Click **"Add new panel"**

## Step 4: Add Dashboard Panels

### Panel 1: API Response Times
1. **Panel Title**: "API Response Times"
2. **Query A**:
   ```
   histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))
   ```
   - **Legend**: `95th percentile - {{endpoint}}`
3. **Query B**:
   ```
   histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, endpoint))
   ```
   - **Legend**: `50th percentile - {{endpoint}}`
4. **Y-axis**: Label = "Response Time (seconds)", Min = 0
5. Click **"Apply"**

### Panel 2: HTTP Request Rate
1. **Panel Title**: "HTTP Request Rate"
2. **Query**:
   ```
   sum(rate(http_requests_total[5m])) by (endpoint)
   ```
   - **Legend**: `{{endpoint}}`
3. **Y-axis**: Label = "Requests per second", Min = 0
4. Click **"Apply"**

### Panel 3: Product Stock Levels
1. **Panel Title**: "Product Stock Levels"
2. **Query**:
   ```
   product_stock_level
   ```
   - **Legend**: `{{product_name}} ({{sku}})`
3. **Y-axis**: Label = "Stock Level", Min = 0
4. Click **"Apply"**

### Panel 4: Business Operations (Stat Panel)
1. **Panel Title**: "Business Operations"
2. **Panel Type**: Change to "Stat"
3. **Query A**:
   ```
   sum(increase(low_stock_alerts_total[1h]))
   ```
   - **Legend**: "Low Stock Alerts (1h)"
4. **Query B**:
   ```
   sum(increase(restock_operations_total[1h]))
   ```
   - **Legend**: "Restock Operations (1h)"
5. **Query C**:
   ```
   sum(increase(product_operations_total[1h])) by (operation_type)
   ```
   - **Legend**: `{{operation_type}} Operations (1h)`
6. Click **"Apply"**

### Panel 5: Container CPU Usage
1. **Panel Title**: "Container CPU Usage"
2. **Query**:
   ```
   rate(container_cpu_usage_seconds_total{container=~"flask-backend.*"}[5m]) * 100
   ```
   - **Legend**: `CPU % - {{pod}}`
3. **Y-axis**: Label = "CPU Usage %", Min = 0, Max = 100
4. Click **"Apply"**

### Panel 6: Container Memory Usage
1. **Panel Title**: "Container Memory Usage"
2. **Query**:
   ```
   container_memory_usage_bytes{container=~"flask-backend.*"} / 1024 / 1024
   ```
   - **Legend**: `Memory MB - {{pod}}`
3. **Y-axis**: Label = "Memory Usage (MB)", Min = 0
4. Click **"Apply"**

## Step 5: Save Dashboard
1. Click **"Save dashboard"** (disk icon)
2. **Dashboard Name**: "Smart Retail Monitoring"
3. **Tags**: Add "inventory" and "api"
4. Click **"Save"**

## Step 6: Set Dashboard Time Range
1. In the top right, set time range to "Last 1 hour"
2. Set refresh rate to "30s"

## Step 7: Generate Data
Run the test script to populate the dashboard with data:
```bash
python3 test_monitoring.py
```

## Troubleshooting

### If Prometheus queries return no data:
1. Check Prometheus targets: http://localhost:9090/targets
2. Verify Flask app is being scraped
3. Check if metrics endpoint is working: http://localhost:5000/metrics

### If dashboard is empty:
1. Make sure you've run the test script to generate data
2. Check the time range (should be "Last 1 hour")
3. Verify the Prometheus data source is working

### Alternative: Import Dashboard JSON
If you prefer, you can import the dashboard JSON directly:
1. Go to **"+"** → **"Import"**
2. Copy and paste the dashboard JSON from `k8s/monitoring/simple-dashboard.json`
3. Click **"Load"** and then **"Import"** 