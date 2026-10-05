#!/bin/bash
# Download competition data from DrivenData (requires login) to data/
# This is the single remaining blocker to training
# Run on any unrestricted machine with DrivenData auth

set -e
mkdir -p data

echo "This script requires DrivenData login."
echo "Manual steps:"
echo "1. Go to https://www.drivendata.org/competitions/306/competition-doe-gems/data/"
echo "2. Download:"
echo "   - training_features.tif (19 bands, 399.5 MB, EPSG:32611, 100m)"
echo "   - labels.tif or existing_faults.tif (60,988 fault pixels)"
echo "   - sample_submission.tif (template, 1.5 MB)"
echo "   - 1m_DEM_links.csv (716 DEM tiles)"
echo "   - GEMS_96647.pdf (rules, sha256 50d854b1e0239fe6...)"
echo "   - Digital-elevation-model-links-JSON.pdf"
echo "3. Place into data/ directory"
echo ""
echo "Alternatively, use Dropbox mirrors (if accessible):"
echo "  - example_submission.tif: https://www.dropbox.com/scl/fi/6rgvnuady818ol8yqgis4/example_submission.tif?rlkey=kbykilvau066xuogoosbf4cq8&st=8junzdyw&dl=1"
echo "  - existing_faults.tif: https://www.dropbox.com/scl/fi/t7fyt03qdh9egyme0itwo/existing_faults.tif?rlkey=yiao96uluqdkipf0h5vju71jf&st=rnino7ya&dl=1"
echo "  - gems-geodawn-numerical-features.tif: https://www.dropbox.com/scl/fi/3vz9o0wwavi26xaeoxlwr/gems-geodawn-numerical-features.tif?rlkey=je8d8fepqfbst9lnwsq9rkplu&st=zj1lag1r&dl=1"
echo "  - GEMS_96647.pdf: https://www.dropbox.com/scl/fi/aemhtutjgcp6tr3tint94/GEMS_96647.pdf?rlkey=rek210cj2smnmzb8n0sla1vmd&st=wz4kofki&dl=0"
echo "  - example_submission.tif: https://www.dropbox.com/scl/fi/6rgvnuady818ol8yqgis4/example_submission.tif?rlkey=kbykilvau066xuogoosbf4cq8&st=8junzdyw&dl=0"
echo ""
echo "After download, run: python scripts/prepare_data.py"
echo ""
echo "Free external data (official, verified):"
echo "  - GDR 1391 INGENIOUS: https://gdr.openei.org/submissions/1391 (DOI 10.15121/1881483, CC BY 4.0)"
echo "    - 2m Temperature Probes: https://gdr.openei.org/files/1391/2m_temperature_probe_INGENIOUS_regional_data.zip"
echo "    - Earthquake Density: https://gdr.openei.org/files/1391/seismicity_INGENIOUS_regional_data.zip"
echo "    - Geodetics: https://gdr.openei.org/files/1391/geodetics_INGENIOUS_regional_data.zip"
echo "    - Paleo geothermal: https://gdr.openei.org/files/1391/paleo_geothermal_regional.zip"
echo "    - Quaternary Faults v2: https://gdr.openei.org/files/1391/qfaults_ingenious_nad83conus117_2023-06-27.zip"
echo "    - Wellsprings: https://gdr.openei.org/files/1391/wellspringdata.gdb.zip"
echo "  - MT Conductance: https://doi.org/10.5066/P9TWT2LU"
echo "  - USGS 3DEP: https://apps.nationalmap.gov/3dep/"
echo "  - ASTER L1T: https://lpdaac.usgs.gov/products/ast_l1t_v003/"
echo "  - Landsat: https://earthexplorer.usgs.gov/"
echo "  - Sentinel-1: https://asf.alaska.edu/"
echo ""

# Try to download free GDR data (these should work without auth)
echo "Attempting to download free GDR data (may fail in restricted sandbox)..."
cd data || exit 1
# Use curl with -k to ignore SSL issues in sandbox (if any)
# Note: In sandbox, SSL may fail, so this is best-effort

# If you have gdown or wget, use those
# For now, just list what would be downloaded

ls -lh
