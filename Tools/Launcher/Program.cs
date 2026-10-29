using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Windows.Forms;

[assembly: AssemblyTitle("Courtroom Chaos")]
[assembly: AssemblyDescription("Launch Courtroom Chaos for Windows")]
[assembly: AssemblyProduct("Courtroom Chaos")]
[assembly: AssemblyVersion("0.1.0.0")]

internal static class Program
{
    [STAThread]
    private static int Main(string[] args)
    {
        string root = AppDomain.CurrentDomain.BaseDirectory;
        string[] locations = {
            Path.Combine(root, "Builds", "Windows", "CourtSimulator.exe"),
            Path.Combine(root, "Game", "CourtSimulator.exe")
        };
        string game = Array.Find(locations, File.Exists);
        if (args.Length == 1 && args[0] == "--check") return game == null ? 1 : 0;
        if (game == null)
        {
            DialogResult result = MessageBox.Show(
                "Download CourtroomChaos-Windows-x64.zip from Releases, extract the entire ZIP, and run CourtroomChaos.exe.\n\n" +
                "Keep the Game folder beside this launcher. In a source checkout, package the project to Builds\\Windows first.\n\nOpen the download page?",
                "Courtroom Chaos - game files needed", MessageBoxButtons.YesNo, MessageBoxIcon.Information);
            if (result == DialogResult.Yes)
                Process.Start(new ProcessStartInfo("https://github.com/AlbertinoTheCoder/Courtroom-Chaos/releases/latest") { UseShellExecute = true });
            return 1;
        }
        try
        {
            Process.Start(new ProcessStartInfo(game) {
                WorkingDirectory = Path.GetDirectoryName(game),
                Arguments = "-windowed -ResX=1280 -ResY=720",
                UseShellExecute = true
            });
            return 0;
        }
        catch (Exception error)
        {
            MessageBox.Show("The game could not start.\n\n" + error.Message,
                "Courtroom Chaos", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return 2;
        }
    }
}
