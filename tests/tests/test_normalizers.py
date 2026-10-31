import pytest

from open_ai_governance_feed.normalizers import normalize_domain


@pytest.mark.parametrize(
    ("input_domain", "expected"),
    [
        ("example.ai", "example.ai"),
        ("Example.AI", "example.ai"),
        (" EXAMPLE.AI ", "example.ai"),
        ("example.ai.", "example.ai"),
        ("www.example.ai", "example.ai"),
        ("WWW.Example.AI.", "example.ai"),
    ],
)
def test_normalize_domain(input_domain, expected):
    assert normalize_domain(input_domain) == expected


def test_normalize_domain_preserves_subdomains():
    assert normalize_domain("chat.example.ai") == "chat.example.ai"
    assert normalize_domain("api.example.ai") == "api.example.ai"


def test_normalize_domain_does_not_parse_urls():
    assert (
        normalize_domain("https://example.ai/tools")
        == "https://example.ai/tools"
    )
