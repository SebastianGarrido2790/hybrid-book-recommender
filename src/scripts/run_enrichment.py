"""
Module for executing the offline data enrichment pipeline.

This script initializes the configuration manager, retrieves the data enrichment
configuration, and executes the enrichment process using the DataEnrichment component.
"""

from src.config.configuration import ConfigurationManager
from src.components.data_enrichment import DataEnrichment
from src.utils.logger import get_logger
import sys

# Standardized logging setup
logger = get_logger(headline="DataEnrichmentScript")


def main():
    try:
        logger.info("🚀 Starting Offline Data Enrichment Process 🚀")

        config_manager = ConfigurationManager()
        enrichment_config = config_manager.get_data_enrichment_config()

        enricher = DataEnrichment(config=enrichment_config)
        enricher.initiate_data_enrichment()

        logger.info("✅ Enrichment Process Completed Successfully ✅")

    except Exception as e:
        logger.error(f"❌ Enrichment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
