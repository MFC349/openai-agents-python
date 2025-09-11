"""Tests for the CLI interface."""

import pytest
from typer.testing import CliRunner

from agents.cli.main import app


class TestCLI:
    """Test CLI functionality."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_cli_help(self):
        """Test CLI help command."""
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "OpenAI Agents SDK with Legendary Training System" in result.stdout
        assert "list-profiles" in result.stdout
        assert "chat" in result.stdout
        assert "demo" in result.stdout
        assert "info" in result.stdout

    def test_list_profiles_command(self):
        """Test list-profiles command."""
        result = self.runner.invoke(app, ["list-profiles"])
        assert result.exit_code == 0
        assert "Available Legendary Training Profiles" in result.stdout
        assert "legendary_sage" in result.stdout
        assert "analytical_master" in result.stdout
        assert "communication_expert" in result.stdout
        assert "innovation_genius" in result.stdout
        assert "ethical_leader" in result.stdout
        assert "balanced_expert" in result.stdout

    def test_info_command(self):
        """Test info command."""
        result = self.runner.invoke(app, ["info"])
        assert result.exit_code == 0
        assert "Legendary AI Training System" in result.stdout
        assert "Key Features" in result.stdout
        assert "Training Intensities" in result.stdout
        assert "Training Focus Areas" in result.stdout

    def test_chat_command_help(self):
        """Test chat command help."""
        result = self.runner.invoke(app, ["chat", "--help"])
        assert result.exit_code == 0
        assert "Chat with a legendary AI agent" in result.stdout
        assert "--message" in result.stdout
        assert "--no-interactive" in result.stdout

    def test_chat_command_invalid_profile(self):
        """Test chat command with invalid profile."""
        result = self.runner.invoke(app, ["chat", "invalid_profile", "-m", "test"])
        assert result.exit_code == 0  # Command runs but shows error
        assert "Error:" in result.stdout
        assert "Unknown profile" in result.stdout

    def test_demo_command_help(self):
        """Test demo command help."""
        result = self.runner.invoke(app, ["demo", "--help"])
        assert result.exit_code == 0
        assert "Run the legendary training system demonstration" in result.stdout
        assert "--profile" in result.stdout

    def test_demo_command_invalid_profile(self):
        """Test demo command with invalid profile."""
        result = self.runner.invoke(app, ["demo", "-p", "invalid_profile"])
        assert result.exit_code == 0  # Command runs but shows error
        assert "Error:" in result.stdout

    def test_demo_command_valid_profile(self):
        """Test demo command with valid profile."""
        # This test may take longer due to stub model processing
        result = self.runner.invoke(app, ["demo", "-p", "communication_expert"])
        assert result.exit_code == 0
        assert "Demonstrating Communication Expert" in result.stdout or "Communication Expert" in result.stdout


class TestCLIAgentInteraction:
    """Test CLI interactions with agents."""

    def setup_method(self):
        """Set up test runner.""" 
        self.runner = CliRunner()

    def test_chat_single_message_communication_expert(self):
        """Test single message chat with communication expert."""
        result = self.runner.invoke(app, [
            "chat", "communication_expert", 
            "-m", "Hello, explain something simple",
            "--no-interactive"
        ])
        assert result.exit_code == 0
        assert "Communication Expert" in result.stdout
        assert "Legendary Agent:" in result.stdout

    def test_chat_single_message_analytical_master(self):
        """Test single message chat with analytical master."""
        result = self.runner.invoke(app, [
            "chat", "analytical_master",
            "-m", "Analyze this situation",
            "--no-interactive"
        ])
        assert result.exit_code == 0
        assert "Analytical Master" in result.stdout

    def test_agent_profile_information_display(self):
        """Test that agent profile information is displayed correctly."""
        result = self.runner.invoke(app, [
            "chat", "innovation_genius",
            "-m", "Quick test",
            "--no-interactive"
        ])
        assert result.exit_code == 0
        assert "Innovation Genius" in result.stdout
        assert "Legendary Agent Ready" in result.stdout
        assert "Intensity:" in result.stdout
        assert "Focus:" in result.stdout
        assert "Domains:" in result.stdout


class TestCLIErrorHandling:
    """Test CLI error handling."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_missing_required_argument(self):
        """Test missing required argument."""
        result = self.runner.invoke(app, ["chat"])
        assert result.exit_code != 0
        assert "Missing argument" in result.stdout

    def test_invalid_command(self):
        """Test invalid command."""
        result = self.runner.invoke(app, ["invalid-command"])
        assert result.exit_code != 0
        assert "No such command" in result.stdout

    def test_chat_without_message_or_interactive(self):
        """Test chat command without message and with no-interactive."""
        result = self.runner.invoke(app, [
            "chat", "legendary_sage", 
            "--no-interactive"
        ])
        # Should complete without starting interactive session
        assert result.exit_code == 0


class TestCLITrainingProfiles:
    """Test CLI training profile handling."""

    def setup_method(self):
        """Set up test runner."""
        self.runner = CliRunner()

    def test_all_predefined_profiles_work_with_cli(self):
        """Test that all predefined profiles work with CLI."""
        profiles = [
            "legendary_sage",
            "analytical_master", 
            "communication_expert",
            "innovation_genius",
            "ethical_leader",
            "balanced_expert"
        ]
        
        for profile in profiles:
            result = self.runner.invoke(app, [
                "chat", profile,
                "-m", f"Test {profile}",
                "--no-interactive"
            ])
            assert result.exit_code == 0, f"Profile {profile} failed"
            assert "Legendary Agent Ready" in result.stdout

    def test_profile_specific_characteristics_shown(self):
        """Test that profile-specific characteristics are shown in CLI."""
        # Test legendary sage - should show comprehensive
        result = self.runner.invoke(app, [
            "chat", "legendary_sage",
            "-m", "Test message",
            "--no-interactive"
        ])
        assert result.exit_code == 0
        assert "comprehensive" in result.stdout.lower()

        # Test analytical master - should show analytical
        result = self.runner.invoke(app, [
            "chat", "analytical_master", 
            "-m", "Test message",
            "--no-interactive"
        ])
        assert result.exit_code == 0
        assert "analytical" in result.stdout.lower()

        # Test communication expert - should show interpersonal
        result = self.runner.invoke(app, [
            "chat", "communication_expert",
            "-m", "Test message", 
            "--no-interactive"
        ])
        assert result.exit_code == 0
        assert "interpersonal" in result.stdout.lower()