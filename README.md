# Doctor Syria Project

## Overview
Doctor Syria is a web application built with Django and React, designed to provide medical services and information.

## Features
- Modern web interface built with React
- Robust backend API with Django
- Real-time monitoring with Prometheus and Grafana
- Automated backups
- Containerized with Docker
- Load balancing with Nginx

## Prerequisites
- Docker and Docker Compose
- Git

## Installation
1. Clone the repository:
```bash
git clone https://github.com/[your-username]/doctor-syria-v2.git
cd doctor-syria-v2
```

2. Create and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Build and start the services:
```bash
docker-compose up -d
```

4. Access the application:
- Web Application: http://localhost
- Grafana Dashboard: http://localhost:3000
- Prometheus: http://localhost:9090
- AlertManager: http://localhost:9093

## Monitoring
The application includes comprehensive monitoring:
- System metrics via Node Exporter
- Container metrics via cAdvisor
- Application metrics via Prometheus
- Visualization through Grafana
- Alerts configuration via AlertManager

## Backup
Automated daily backups are configured for the database. Backups are stored in the `backups` directory and are retained for 7 days.

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
