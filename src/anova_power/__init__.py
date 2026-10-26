"""anova_power — tek yönlü ANOVA güç analizi.

Hesap mantığının tamamı `core` modülündedir (ödev kuralı 3). `cli` ve
`mcp_server` yalnızca bu motoru çağıran ince katmanlardır.
"""
from .core import MAX_N, analyze, number, statistics

__all__ = ["MAX_N", "analyze", "number", "statistics"]
__version__ = "1.0.0"
