# Project Summary

## Overview
This project aims to build a robust and professional algorithmic trading bot using NautilusTrader and Interactive Brokers (IB). The setup showcases modern software engineering best practices, emphasizing maintainability, cost-efficiency, and scalability. The bot will be deployed in two different Google Cloud Platform (GCP) setups for cost and execution comparisons:

1. **Serverless Container Execution (Cloud Run)**: Scheduled daily execution using Docker containers for rapid startup, optimal cost efficiency, and minimal runtime.
2. **Continuous VM Deployment (Compute Engine)**: A virtual machine running continuously (24/7) to assess the trade-off between execution flexibility and ongoing costs.

## Project Structure
```
nautilus_trading_bot/
├── README.md                   # Project overview and setup instructions
├── .gitignore                  # Git ignore rules
├── pyproject.toml              # Dependency management (uv)
├── uv.lock                     # Locked dependencies
├── Dockerfile                  # Docker container definition
├── .github/
│   └── workflows/
│       └── ci_cd.yml           # GitHub Actions Continuous Integration
├── scripts/
│   └── startup.sh              # VM startup automation script
└── src/
    ├── main.py                 # Entry point for trading bot
    ├── config/                 # Environment-specific configs
    ├── data_ingestion/         # Market data retrieval and preprocessing
    ├── strategies/             # Algorithmic trading strategies
    ├── execution/              # Order placement and risk management
    ├── backtesting/            # Historical simulation and evaluation
    └── utils/                  # Common reusable components
```

## Technologies & Services
- **NautilusTrader:** Core trading platform
- **Interactive Brokers (IB):** Broker API integration
- **Google Cloud Platform:**
  - Compute Engine (VM Instance)
  - Cloud Run (Serverless Docker)
  - Cloud Scheduler (Task Scheduling)
- **Docker:** Containerized environment
- **GitHub Actions:** Continuous Integration & Deployment (CI/CD)
- **uv (Astral):** Python dependency management

## Deployment Strategies
- **Cloud Run (Serverless):**
  - Minimal costs; only pay for container runtime.
  - Daily scheduled task execution.

- **Compute Engine (VM):**
  - 24/7 runtime; greater responsiveness but ongoing cost implications.
  - Automated VM management via startup/shutdown scripts.

## Future Enhancements
- Integrate MLFlow for experiment tracking.
- Expand to multiple concurrent bots for diversified strategies.
- Explore infrastructure automation options.

This approach highlights cost-effective resource utilization, best DevOps practices, and provides a foundation for scalable and sophisticated trading strategies.

