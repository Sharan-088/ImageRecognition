# ⚡ GPU Setup Guide for NVIDIA RTX 3050 Ti

## Your System
- **GPU:** NVIDIA GeForce RTX 3050 Ti (4-6GB VRAM)
- **Issue:** Currently using CPU instead of GPU
- **Goal:** Use GPU to train 6-10x faster

---

## ⚡ Quick Setup (5 Steps)

### Step 1: Install NVIDIA Driver
```bash
# Option A: Use GeForce Experience app (easiest)
# - Open GeForce Experience
# - Click "Driver" tab
# - Click "Check for updates"
# - Install if available

# Option B: Manual download
# Visit: https://www.nvidia.com/Download/driverDetails.aspx
# Select your GPU and download latest driver
```

### Step 2: Install CUDA Toolkit 12.4
```bash
# Download from: https://developer.nvidia.com/cuda-downloads
# Select: Windows, x86_64, Windows, .exe (local)
# Run installer and use default path:
# C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.4
```

### Step 3: Download and Extract cuDNN
```bash
# 1. Visit: https://developer.nvidia.com/cudnn
# 2. Create free NVIDIA account
# 3. Download "cuDNN for Windows"
# 4. Extract ZIP file
# 5. Copy contents to CUDA folder:
#    C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.4\
```

### Step 4: Add CUDA to Windows PATH
```bash
# 1. Open: Settings → System → About → Advanced system settings
# 2. Click "Environment Variables"
# 3. Under "System variables", click "New"
# 4. Variable name: CUDA_PATH
# 5. Variable value: C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.4
# 6. Click OK twice
# 7. RESTART YOUR COMPUTER (IMPORTANT!)
```

### Step 5: Install TensorFlow with GPU Support
```bash
# Activate virtual environment
venv\Scripts\activate

# Remove old TensorFlow
pip uninstall tensorflow -y

# Install GPU version
pip install tensorflow[and-cuda]

# This takes 5-10 minutes (larger download)
```

---

## ✅ Verify GPU Setup

### Test 1: Quick Check
```bash
venv\Scripts\activate
python test_gpu.py
```

**Expected output:**
```
Physical Devices:
  • /physical_device:GPU:0

GPU Devices:
✓ GPU Detected: 1 GPU(s)
  ✓ /physical_device:GPU:0

✓ GPU computation successful!
✓✓✓ GPU IS READY FOR TRAINING! ✓✓✓
```

### Test 2: Train with GPU
```bash
python train_gpu.py
```

**Expected output:**
```
GPU Configuration
✓ GPU Detected: 1 GPU(s)
  • /physical_device:GPU:0
✓ Using GPU for training!

STARTING GPU-ACCELERATED TRAINING
✓ TRAINING COMPLETED
  Total time: 2.5 minutes (instead of 15-20 minutes!)
```

---

## 🚀 Training Speed Comparison

### Your RTX 3050 Ti Expected Performance

| Task | CPU | GPU | Speedup |
|------|-----|-----|---------|
| 20 epochs training | 15-20 min | 2-3 min | **6-10x** |
| Single prediction | 1 sec | 0.2 sec | **5x** |
| 300 images total | ~18 min | ~2.5 min | **7x** |

---

## 🎯 Training Commands

### Option 1: Use GPU (Recommended)
```bash
venv\Scripts\activate
python train_gpu.py
```

**Features:**
- ✓ Automatic GPU detection
- ✓ GPU memory optimization
- ✓ Training time display
- ✓ Faster 6-10x training

### Option 2: Original Training (CPU)
```bash
venv\Scripts\activate
python train.py
```

---

## 🛑 Troubleshooting

### "GPU not detected" after setup
```bash
# 1. Restart computer (CRITICAL!)
# 2. Verify CUDA installed:
dir "C:\Program Files\NVIDIA GPU Computing Toolkit"

# 3. Verify cuDNN extracted:
dir "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.4\bin" | find "cudnn"

# 4. Test again:
python test_gpu.py
```

### "CUDA not found" error
```bash
# Add CUDA to system PATH and restart:
# Settings → System → About → Advanced system settings
# → Environment Variables → New
# → CUDA_PATH = C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.4
```

### "Could not load cudart64_*.dll"
```bash
# Reinstall with:
pip uninstall tensorflow -y
pip install tensorflow[and-cuda] --force-reinstall
```

### GPU runs out of memory
```bash
# In train_gpu.py, reduce batch size:
BATCH_SIZE = 16  # (instead of 32)
```

---

## 📊 Monitor GPU During Training

### Method 1: Windows Task Manager
1. Open Task Manager (Ctrl + Shift + Esc)
2. Go to "Performance" tab
3. Click "GPU"
4. Watch usage while training (should show 70-90%)

### Method 2: NVIDIA GeForce Experience
1. Open NVIDIA GeForce Experience
2. Enable "Performance Overlay"
3. Run training and check overlay

---

## ✅ GPU Setup Checklist

Before training, verify:

- [ ] NVIDIA driver installed
- [ ] CUDA 12.4 installed
- [ ] cuDNN extracted
- [ ] CUDA added to PATH
- [ ] Computer restarted
- [ ] `test_gpu.py` runs with GPU
- [ ] `train_gpu.py` shows GPU usage
- [ ] Task Manager shows GPU activity

---

## 🎓 Key Files

| File | Purpose |
|------|---------|
| `train_gpu.py` | GPU-optimized training script |
| `test_gpu.py` | Verify GPU is working |
| `train.py` | Original CPU training script |

---

## 📞 Still Not Working?

1. **Check GPU in Device Manager:**
   - Right-click Windows Start
   - Select "Device Manager"
   - Look for "NVIDIA GeForce RTX 3050 Ti"
   - If yellow warning: Driver issue

2. **Check CUDA installation:**
   - Open Command Prompt
   - Run: `nvcc --version`
   - Should show CUDA version

3. **Reinstall TensorFlow:**
   ```bash
   pip uninstall tensorflow -y
   pip install tensorflow[and-cuda] --upgrade
   ```

4. **Force GPU usage test:**
   ```python
   # In Python:
   import tensorflow as tf
   print(tf.config.list_physical_devices('GPU'))
   ```

---

## 🚀 Once GPU is Ready

```bash
# 1. Activate environment
venv\Scripts\activate

# 2. Run GPU training
python train_gpu.py

# 3. Watch the magic happen!
# Training should complete in 2-3 minutes instead of 15-20 minutes

# 4. Use trained model
python app.py
```

**Estimated total GPU setup time: 30-45 minutes**
**Time saved per training cycle: 12-17 minutes**

---

## 💡 Important Notes

- **CUDA is required** - TensorFlow needs it for GPU support
- **cuDNN is required** - Library for GPU operations
- **Driver must be updated** - Use GeForce Experience
- **PATH restart is critical** - Windows won't find CUDA without it
- **RTX 3050 Ti is perfect** - Great for ML training
- **4-6GB VRAM is enough** - For this project

---

**Ready to train faster? Follow the 5 steps above!** 🚀
