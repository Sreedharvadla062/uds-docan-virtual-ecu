# Contributing to UDS DoCAN Virtual ECU

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Request Process

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Make sure your code lints.
5. Issue that pull request!

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Document functions with docstrings
- Write clear commit messages

### Testing

We use pytest for testing. Before submitting:

```bash
pip install -r requirements-dev.txt
pytest tests/ --cov=src
black src/ tests/
flake8 src/ tests/
mypy src/
```

## Reporting Bugs

When reporting bugs, please include:

- Python version and OS
- Detailed description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Code snippets or error traces

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to making participation in our project and our community a harassment-free experience for everyone.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing opinions and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

## Questions?

Feel free to open an issue with your question!
