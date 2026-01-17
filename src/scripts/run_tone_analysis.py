from src.config.configuration import ConfigurationManager
from src.components.tone_analysis import ToneAnalysis
from src.utils.logger import get_logger
import sys

# Standardized logging setup
logger = get_logger(__name__, headline="ToneAnalysisScript")


def main():
    try:
        logger.info("🚀 Starting Offline Tone Analysis Process 🚀")

        config_manager = ConfigurationManager()
        tone_config = config_manager.get_tone_analysis_config()

        analyzer = ToneAnalysis(config=tone_config)
        analyzer.initiate_tone_analysis()

        logger.info("✅ Tone Analysis Completed Successfully ✅")

    except Exception as e:
        logger.error(f"❌ Tone Analysis failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
