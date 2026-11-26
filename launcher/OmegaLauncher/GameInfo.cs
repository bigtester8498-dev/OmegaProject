namespace OmegaLauncher
{
    /// <summary>
    /// Every game-specific name the launcher uses, in one place. The values follow the Names table in the
    /// repository's CLAUDE.md; change them there first, then here. The rest of the launcher reads them from here
    /// (MSBuild names such as the assembly name and the product name are in OmegaLauncher.csproj).
    /// </summary>
    public static class GameInfo
    {
        /// <summary>The game's name as shown to the player.</summary>
        public const string DisplayName = "Omega";

        /// <summary>Window title of the launcher, Russian and English.</summary>
        public const string WindowTitleRu = "Лаунчер " + DisplayName;

        public const string WindowTitleEn = DisplayName + " Launcher";

        /// <summary>The game executable in the game folder.</summary>
        public const string GameExe = "Omega.exe";

        /// <summary>Unity's data folder beside the game executable.</summary>
        public const string DataFolder = "Omega_Data";

        /// <summary>Unity companyName and productName: persistentDataPath is LocalLow\Company\Product\.</summary>
        public const string CompanyName = "OmegaProject";

        public const string ProductName = "Omega";

        /// <summary>The download site (GitHub Pages of the repository). Must end with a slash.</summary>
        public const string DefaultBaseUrl = "https://bigtester8498-dev.github.io/OmegaProject/";

        /// <summary>The launcher's own executable name, also the file name in launcher-version.json.</summary>
        public const string LauncherExe = "OmegaLauncher.exe";

        /// <summary>The launcher's working folder next to the launcher (downloads, staging, install record).</summary>
        public const string StateFolder = ".omega";

        /// <summary>The base content package (Content/core): always on, never listed as a mod.</summary>
        public const string BasePackageId = "core";

        /// <summary>HTTP User-Agent of the launcher's requests.</summary>
        public const string UserAgent = "OmegaLauncher";

        /// <summary>Prefix of the temp folder a launcher self-update downloads into.</summary>
        public const string TempPrefix = "omega-launcher-";

        /// <summary>Logical name of the embedded icon (see OmegaLauncher.csproj).</summary>
        public const string IconResource = "OmegaLauncher.omega.ico";

        /// <summary>Environment variable with an extra UI scale factor (layout checks at 125% and 150%).</summary>
        public const string UiScaleVariable = "OMEGA_UI_SCALE";
    }
}
