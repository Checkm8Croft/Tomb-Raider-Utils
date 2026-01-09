using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Controls.Primitives;
using Microsoft.UI.Xaml.Data;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media;
using Microsoft.UI.Xaml.Navigation;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.Storage.Pickers;
using WinRT.Interop;
using IWshRuntimeLibrary;
using System.IO;
using Microsoft.UI.Windowing;

namespace Tomb_Raider_Shortcut_Maker
{
    public sealed partial class MainWindow : Window
    {
        private void SetWindowSize(int width, int height)
        {
            var hwnd = WindowNative.GetWindowHandle(this);
            var windowId = Microsoft.UI.Win32Interop.GetWindowIdFromWindow(hwnd);
            var appWindow = AppWindow.GetFromWindowId(windowId);

            appWindow.Resize(new Windows.Graphics.SizeInt32(width, height));
        }

        public MainWindow()
        {
            this.InitializeComponent();
            SetWindowSize(520, 400);
        }

        private async void BrowsePath(object sender, RoutedEventArgs e)
        {
            var picker = new FileOpenPicker();

            // Associa il picker alla finestra WinUI
            var hwnd = WindowNative.GetWindowHandle(this);
            InitializeWithWindow.Initialize(picker, hwnd);

            picker.FileTypeFilter.Add(".exe");

            var file = await picker.PickSingleFileAsync();
            if (file != null)
            {
                ExePathBox.Text = file.Path;
            }
        }

        private string selectedArgument = "";
        private void Args(object sender, RoutedEventArgs e)
        {
            ArgumentComboBox.IsEnabled = true;
        }
        private void NoArgs(object sender, RoutedEventArgs e)
        {
            ArgumentComboBox.IsEnabled = false;
            selectedArgument = "";
        }

        private void Argument(object sender, SelectionChangedEventArgs e)
        {
            if (ArgumentComboBox.SelectedItem is string arg)
            {
                selectedArgument = arg;
            }
        }
        private async void ShowError(string message)
        {
            var dialog = new ContentDialog
            {
                Title = "Error",
                Content = message,
                CloseButtonText = "OK",
                XamlRoot = this.Content.XamlRoot
            };
            await dialog.ShowAsync();
        }

        private async void ShowSuccess(string message)
        {
            var dialog = new ContentDialog
            {
                Title = "Done",
                Content = message,
                CloseButtonText = "OK",
                XamlRoot = this.Content.XamlRoot
            };
            await dialog.ShowAsync();
        }

        private void CreateShortcut_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrWhiteSpace(ExePathBox.Text) ||
                string.IsNullOrWhiteSpace(ShortcutPathBox.Text))
            {
                ShowError("Select both the executable and the destination folder.");
                return;
            }

            var exePath = ExePathBox.Text;
            var shortcutDir = ShortcutPathBox.Text;

            if (!System.IO.File.Exists(exePath) || !Directory.Exists(shortcutDir))
            {
                ShowError("Invalid path selected.");
                return;
            }

            var baseName = Path.GetFileNameWithoutExtension(exePath);
            var shortcutName = baseName;

            // LOGICA NOME + ARGOMENTI
            if (UseArgumentCheckBox.IsChecked == true && !string.IsNullOrEmpty(selectedArgument))
            {
                if (selectedArgument == "-gold")
                    shortcutName += " Gold";
                else if (selectedArgument == "-setup")
                    shortcutName += " Setup";
            }
            else
            {
                selectedArgument = "";
            }

            var shortcutPath = Path.Combine(shortcutDir, $"{shortcutName}.lnk");

            var shell = new WshShell();
            IWshShortcut shortcut = (IWshShortcut)shell.CreateShortcut(shortcutPath);

            shortcut.TargetPath = exePath;
            shortcut.WorkingDirectory = Path.GetDirectoryName(exePath);

            if (!string.IsNullOrEmpty(selectedArgument))
                shortcut.Arguments = selectedArgument;

            shortcut.Save();

            ShowSuccess("Shortcut created successfully.");
        }



        private async void BrowseShortcutPath(object sender, RoutedEventArgs e)
        {
            var picker = new FolderPicker();

            var hwnd = WindowNative.GetWindowHandle(this);
            InitializeWithWindow.Initialize(picker, hwnd);

            picker.FileTypeFilter.Add("*");

            var folder = await picker.PickSingleFolderAsync();
            if (folder != null)
            {
                ShortcutPathBox.Text = folder.Path;
            }
        }

    }
}
