# 🚀 Quick Start: Upload & Run Smart Retail App After Reboot

Follow these steps to get your Smart Retail App up and running after a fresh reboot.

---

## 1. Open Terminal and Go to Project Directory
```sh
cd /Users/litalhay/dev/smart-retail-app
```

---

## 2. (Optional) Kill Any Stale Port-Forward Processes
If you had port-forwards running before reboot, clear them:
```sh
pkill -f "kubectl port-forward"
```

---

## 3. (If Using Minikube or Local K8s) Start Your Kubernetes Cluster
If you use Minikube:
```sh
minikube start
minikube addons enable ingress
```
If you use another local K8s, start it as appropriate.

---

## 4. Deploy All Kubernetes Resources
```sh
kubectl apply -f k8s/configs/
kubectl apply -f k8s/secrets/
kubectl apply -f k8s/services/
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/ingress/
kubectl apply -f k8s/monitoring/
```

---

## 5. Start Port Forwarding for Backend and Monitoring
```sh
kubectl port-forward service/flask-service 5000:5000 &
kubectl port-forward service/grafana-service 3001:3000 &
kubectl port-forward service/prometheus-service 9090:9090 &
```
If you get connection refused errors, wait a few seconds and try again. Make sure the pods are running:
```sh
kubectl get pods
```
All pods should be in the `Running` state.

Run the docker 
```sh
docker-compose up
```

If you want to access the backend from outside Docker or from another device, make sure Flask is running on 0.0.0.0:
```sh
flask run --host=0.0.0.0
```
---

## 6. Start the React Frontend
Open a new terminal tab/window:
```sh
cd /Users/litalhay/dev/smart-retail-app/frontend
npm install
npm start
```

---

## 7. Access the Application
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000
- **Grafana:** http://localhost:3001 (login: admin/admin123)
- **Prometheus:** http://localhost:9090

---

## 8. (Optional) Load Sample Data
If you want to load sample products:
```sh
./update_sample_data.sh
# Or, for API-based loading:
python3 load_via_api.py
```

---

## 9. (Optional) Run Health Checks and Tests on /scripts
```sh
python3 health_check.py
python3 test_monitoring.py
```

---

## 10. (Optional) View Logs and Status
```sh
kubectl get all
kubectl logs -f deployment/flask-deployment
```

---

## 11. (Optional) Stop Port Forwarding
When you’re done:
```sh
pkill -f "kubectl port-forward"
```

---

## Troubleshooting

- **Pods not running:**  
  Check with `kubectl get pods` and inspect logs with `kubectl logs <pod-name>`.
- **Port forwarding errors:**  
  Make sure pods are running and try port-forward again.
- **Database issues:**  
  Check Postgres pod and logs.

---

## Quick Reference

| Step | Command/Action |
|------|---------------|
| Go to project root | `cd /Users/litalhay/dev/smart-retail-app` |
| Kill old port-forwards | `pkill -f "kubectl port-forward"` |
| Start K8s (if needed) | `minikube start` |
| Deploy K8s resources | `kubectl apply -f k8s/...` |
| Start port-forwarding | `kubectl port-forward service/flask-service 5000:5000 &`<br>`kubectl port-forward service/grafana-service 3001:3000 &`<br>`kubectl port-forward service/prometheus-service 9090:9090 &` |
| Start frontend | `cd frontend && npm install && npm start` |
| Load sample data | `./update_sample_data.sh` or `python3 load_via_api.py` |
| Health check | `python3 health_check.py` |
| Stop port-forwards | `pkill -f "kubectl port-forward"` |

---

**If you encounter any specific errors, check the logs and pod status, or refer to `docs/COMPLETE_GUIDE.md` for more details.** 

---

To access Grafana, follow these steps:

Open Grafana in Your Browser

Go to:
```
http://localhost:3001
```

---

### 3. Log In

- **Default username:** `admin`
- **Default password:** `admin123` (unless you changed it in your secrets/config)

---

### 4. Explore Dashboards

- Once logged in, you can view the pre-configured dashboards, add new ones, or import dashboards (such as your `simple-dashboard.json`).

---

### Troubleshooting

- If you get a connection error, make sure:
  - The Grafana pod is running:  
    ```sh
    kubectl get pods | grep grafana
    ```
    The status should be `Running`.
  - The port-forward command is running and not showing errors.
- If you changed the port, adjust the URL accordingly.

---