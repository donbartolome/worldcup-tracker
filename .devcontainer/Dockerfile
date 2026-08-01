FROM mcr.microsoft.com/devcontainers/python:3.14

# Keep claude-code pinned to the version declared in devcontainer-lock.json
# instead of letting it silently drift via auto-update.
ENV DISABLE_AUTOUPDATER=1

# Compose mounts named volumes onto these paths; without pre-creating them
# Docker initializes them root-owned and vscode-run processes can't write.
RUN mkdir -p /home/vscode/.claude && chown vscode:vscode /home/vscode/.claude
RUN mkdir -p /home/vscode/.config/gh && chown vscode:vscode /home/vscode/.config/gh
