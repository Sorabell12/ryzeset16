<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quét Hàng Hóa - Định Vị Phường Nha Trang (Cũ)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f3f4f6; }
        .camera-container { position: relative; width: 100%; max-width: 500px; margin: 0 auto; border-radius: 1rem; overflow: hidden; background: #000; aspect-ratio: 3/4;}
        video { width: 100%; height: 100%; object-fit: cover; }
        .overlay { position: absolute; inset: 0; pointer-events: none; border: 2px solid rgba(255, 255, 255, 0.2); }
        .scan-box { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 80%; height: 120px; border: 2px dashed #4ade80; border-radius: 0.5rem; background: rgba(74, 222, 128, 0.1); }
        .scanning-line { width: 100%; height: 2px; background-color: #4ade80; position: absolute; top: 0; left: 0; animation: scan 2s infinite linear; }
        @keyframes scan { 0% { top: 0; } 50% { top: 100%; } 100% { top: 0; } }
        #canvas { display: none; }
    </style>
</head>
<body class="flex flex-col min-h-screen">

    <header class="bg-blue-700 text-white p-4 shadow-md text-center">
        <h1 class="text-xl font-bold"><i class="fa-solid fa-map-location-dot mr-2"></i>Phân Loại Phường Nha Trang</h1>
        <p class="text-xs text-blue-200 mt-1">Hệ thống áp dụng chuẩn Phường Cũ (trước sáp nhập)</p>
    </header>

    <main class="flex-grow p-4 flex flex-col items-center w-full max-w-lg mx-auto">
        
        <!-- Camera Section -->
        <div class="camera-container shadow-lg mb-4">
            <video id="video" autoplay playsinline></video>
            <div class="overlay">
                <div class="scan-box" id="scan-box">
                    <div class="scanning-line hidden" id="scan-line"></div>
                </div>
            </div>
            <!-- Loading Indicator for OCR -->
            <div id="loading-overlay" class="absolute inset-0 bg-black bg-opacity-70 flex flex-col items-center justify-center text-white hidden">
                <i class="fa-solid fa-spinner fa-spin text-4xl text-green-400 mb-2"></i>
                <p class="text-sm" id="loading-text">Đang phân tích hình ảnh...</p>
            </div>
        </div>

        <div class="flex space-x-3 w-full mb-6">
            <button id="capture-btn" class="flex-1 bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-xl shadow-md transition-transform transform active:scale-95 flex items-center justify-center text-sm">
                <i class="fa-solid fa-camera mr-2"></i> Chụp Quét
            </button>
            <button id="auto-scan-btn" class="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-bold py-3 px-4 rounded-xl shadow-md transition-transform transform active:scale-95 flex items-center justify-center text-sm">
                <i class="fa-solid fa-bolt mr-2"></i> Quét Tự Động
            </button>
        </div>

        <canvas id="canvas"></canvas>

        <!-- Result Card -->
        <div id="result-card" class="w-full bg-white rounded-xl shadow-md p-5 mb-4 hidden border-l-4 border-blue-500">
            <h2 class="text-lg font-bold text-gray-800 mb-2 border-b pb-2"><i class="fa-solid fa-boxes-packing text-blue-500 mr-2"></i>Kết Quả Phân Loại</h2>
            <div class="space-y-2 mt-3">
                <p class="text-sm text-gray-600">Văn bản quét được: <span id="raw-text" class="font-mono text-gray-900 bg-gray-100 p-1 rounded block mt-1 break-words italic"></span></p>
                <div class="flex items-center justify-between bg-blue-50 p-3 rounded-lg">
                    <span class="text-sm font-semibold text-gray-700">Tên đường:</span>
                    <span id="res-street" class="font-bold text-blue-700 text-right">---</span>
                </div>
                <div class="flex items-center justify-between bg-blue-50 p-3 rounded-lg">
                    <span class="text-sm font-semibold text-gray-700">Số nhà:</span>
                    <span id="res-number" class="font-bold text-blue-700 text-right">---</span>
                </div>
                <div class="flex flex-col bg-green-50 p-3 rounded-lg border border-green-200 mt-2">
                    <span class="text-xs font-semibold text-gray-500 uppercase">Thuộc phường (Cũ):</span>
                    <span id="res-ward" class="font-bold text-green-700 text-xl mt-1"><i class="fa-solid fa-check-circle mr-1"></i> ---</span>
                </div>
            </div>
        </div>

        <!-- Manual Override / Testing Section -->
        <div class="w-full bg-white rounded-xl shadow-md p-5 border border-gray-200">
            <h3 class="text-sm font-bold text-gray-700 mb-3"><i class="fa-solid fa-keyboard mr-2"></i>Nhập Thủ Công (Để Kiểm Tra)</h3>
            <div class="flex space-x-2">
                <input type="text" id="manual-address" placeholder="VD: 155 Thống Nhất" class="flex-grow border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500">
                <button id="manual-btn" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold shadow transition-colors">
                    Kiểm tra
                </button>
            </div>
            <p class="text-xs text-gray-400 mt-2">*Hệ thống giả lập dữ liệu cho đường Thống Nhất, Lê Hồng Phong, Thái Nguyên.</p>
        </div>

    </main>

    <script>
        // Cơ sở dữ liệu MOCK mô phỏng phân tách phường cũ dựa trên số nhà
        // Việc thiết lập này giả định các quy tắc chẵn/lẻ hoặc khoảng số
        const NHA_TRANG_WARD_DB = {
            "thong nhat": {
                name: "Thống Nhất",
                rules: [
                    // Giả lập: Số từ 1 đến 150 thuộc Vạn Thạnh cũ, từ 151 trở lên thuộc Phương Sài cũ
                    { min: 1, max: 150, ward: "Vạn Thạnh (Chưa sáp nhập)" },
                    { min: 151, max: 9999, ward: "Phương Sài (Chưa sáp nhập)" }
                ]
            },
            "le hong phong": {
                name: "Lê Hồng Phong",
                rules: [
                    // Giả lập: Đường rất dài cắt qua nhiều phường
                    { min: 1, max: 200, ward: "Phước Hải (Cũ)" },
                    { min: 201, max: 500, ward: "Phước Tân (Cũ)" },
                    { min: 501, max: 9999, ward: "Phước Long" }
                ]
            },
            "thai nguyen": {
                name: "Thái Nguyên",
                rules: [
                    { type: "even", min: 2, max: 100, ward: "Phước Tân (Cũ)" },
                    { type: "odd", min: 1, max: 99, ward: "Phương Sài (Cũ)" }
                ]
            }
        };

        // Utility to remove Vietnamese accents for easier matching
        function removeAccents(str) {
            return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
        }

        // Logic phân tích và tra cứu
        function parseAndLookupAddress(rawText) {
            // Regex cơ bản để tìm Số nhà và phần Tên đường phía sau
            // Ví dụ: "Số 155 Thống Nhất, Nha Trang" -> Match: 155, Thống Nhất
            const regex = /(?:số\s*)?(\d+)[a-zA-Z\/\-]*\s+([a-zA-ZÀ-ỹ\s]+)/i;
            const match = rawText.match(regex);

            if (!match) {
                return { error: "Không tìm thấy cấu trúc 'Số nhà + Tên đường' trong ảnh." };
            }

            const houseNum = parseInt(match[1], 10);
            let streetNameRaw = match[2].trim();
            
            // Xóa chữ "đường" hoặc "phố" ở đầu nếu có
            streetNameRaw = streetNameRaw.replace(/^(đường|phố)\s+/i, '');

            const cleanStreetName = removeAccents(streetNameRaw);
            let matchedWard = "Không xác định hoặc phường mặc định";
            let dbStreetName = streetNameRaw;

            // Tìm kiếm trong DB
            let found = false;
            for (const [key, data] of Object.entries(NHA_TRANG_WARD_DB)) {
                // Kiểm tra xem chuỗi tên đường quét được có chứa tên đường trong DB không
                if (cleanStreetName.includes(key)) {
                    found = true;
                    dbStreetName = data.name;
                    // Lọc qua các rule số nhà
                    for (const rule of data.rules) {
                        if (rule.type === 'even' && houseNum % 2 !== 0) continue;
                        if (rule.type === 'odd' && houseNum % 2 === 0) continue;
                        
                        if (houseNum >= rule.min && houseNum <= (rule.max || 99999)) {
                            matchedWard = rule.ward;
                            break;
                        }
                    }
                    break;
                }
            }

            if (!found) {
                 return { 
                    number: houseNum, 
                    street: dbStreetName, 
                    ward: "Chưa có dữ liệu ranh giới trong hệ thống",
                    warning: true 
                };
            }

            return { number: houseNum, street: dbStreetName, ward: matchedWard };
        }

        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const captureBtn = document.getElementById('capture-btn');
        const autoScanBtn = document.getElementById('auto-scan-btn');
        const scanLine = document.getElementById('scan-line');
        const loadingOverlay = document.getElementById('loading-overlay');
        const loadingText = document.getElementById('loading-text');
        const resultCard = document.getElementById('result-card');

        // Khởi động Camera
        async function initCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    video: { facingMode: 'environment' } // Ưu tiên camera sau
                });
                video.srcObject = stream;
            } catch (err) {
                console.error("Lỗi truy cập camera: ", err);
                alert("Không thể truy cập camera. Vui lòng kiểm tra quyền trình duyệt.");
            }
        }

        window.onload = () => {
            initCamera();
        };

        let isProcessing = false;
        let autoScanInterval = null;

        async function executeScan() {
            if (!video.srcObject || isProcessing) return;
            isProcessing = true;

            // Chụp khung hình từ Video
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, canvas.width, canvas.height);

            // Cập nhật UI trạng thái
            scanLine.classList.remove('hidden');
            // Chỉ hiện overlay che đen màn hình nếu đang quét thủ công
            if (!autoScanInterval) {
                loadingOverlay.classList.remove('hidden'); 
            }
            resultCard.classList.add('hidden');
            
            try {
                const dataUrl = canvas.toDataURL('image/jpeg');
                
                // Khởi chạy Tesseract.js (Nhận diện tiếng Việt)
                const result = await Tesseract.recognize(
                    dataUrl,
                    'vie', // Ngôn ngữ Tiếng Việt
                    { logger: m => {
                        if(m.status === 'recognizing text' && !autoScanInterval){
                            loadingText.innerText = `Đang phân tích chữ... ${Math.round(m.progress * 100)}%`;
                        }
                    }}
                );

                const extractedText = result.data.text.trim();
                
                if(!extractedText) {
                    if (!autoScanInterval) {
                        showResult(extractedText, {error: "Không nhận diện được chữ trên ảnh. Hãy thử đưa máy gần hơn và đảm bảo đủ sáng."});
                    }
                } else {
                    const parsedData = parseAndLookupAddress(extractedText);
                    
                    // Nếu đang quét tự động và không tìm thấy đường trong DB, cứ âm thầm quét tiếp
                    if (autoScanInterval && (parsedData.error || parsedData.warning)) {
                        // Không làm gì, bỏ qua khung hình này
                    } else {
                        showResult(extractedText, parsedData);
                        // Nếu quét tự động thành công ra kết quả, tự động dừng quét
                        if (autoScanInterval && !parsedData.error && !parsedData.warning) {
                            toggleAutoScan();
                        }
                    }
                }

            } catch (error) {
                console.error(error);
                if (!autoScanInterval) {
                    showResult("", {error: "Có lỗi xảy ra trong quá trình nhận diện (OCR)."});
                }
            } finally {
                scanLine.classList.add('hidden');
                loadingOverlay.classList.add('hidden');
                loadingText.innerText = 'Đang phân tích hình ảnh...';
                isProcessing = false;
            }
        }

        function toggleAutoScan() {
            if (autoScanInterval) {
                // Tắt quét tự động
                clearInterval(autoScanInterval);
                autoScanInterval = null;
                autoScanBtn.innerHTML = '<i class="fa-solid fa-bolt mr-2"></i> Quét Tự Động';
                autoScanBtn.classList.replace('bg-yellow-500', 'bg-gray-600');
                autoScanBtn.classList.replace('hover:bg-yellow-600', 'hover:bg-gray-700');
                scanLine.classList.add('hidden');
            } else {
                // Bật quét tự động
                executeScan(); // Chạy ngay lập tức 1 lần
                autoScanInterval = setInterval(executeScan, 2000); // Lặp lại mỗi 2 giây
                autoScanBtn.innerHTML = '<i class="fa-solid fa-stop mr-2"></i> Dừng Tự Động';
                autoScanBtn.classList.replace('bg-gray-600', 'bg-yellow-500');
                autoScanBtn.classList.replace('hover:bg-gray-700', 'hover:bg-yellow-600');
                scanLine.classList.remove('hidden');
            }
        }

        captureBtn.addEventListener('click', executeScan);
        autoScanBtn.addEventListener('click', toggleAutoScan);

        // Xử lý nút nhập thủ công
        document.getElementById('manual-btn').addEventListener('click', () => {
            const val = document.getElementById('manual-address').value;
            if(!val) return;
            const parsedData = parseAndLookupAddress(val);
            showResult(val, parsedData);
        });

        function showResult(rawText, data) {
            resultCard.classList.remove('hidden');
            document.getElementById('raw-text').innerText = rawText || "(Không có văn bản)";
            
            if (data.error) {
                document.getElementById('res-street').innerText = "Lỗi";
                document.getElementById('res-number').innerText = "Lỗi";
                document.getElementById('res-ward').innerHTML = `<i class="fa-solid fa-triangle-exclamation text-red-500 mr-1"></i> <span class="text-red-600 text-base">${data.error}</span>`;
                return;
            }

            document.getElementById('res-street').innerText = data.street;
            document.getElementById('res-number').innerText = data.number;
            
            const wardElem = document.getElementById('res-ward');
            if(data.warning) {
                wardElem.innerHTML = `<i class="fa-solid fa-circle-info text-yellow-500 mr-1"></i> <span class="text-yellow-700 text-base">${data.ward}</span>`;
            } else {
                wardElem.innerHTML = `<i class="fa-solid fa-check-circle text-green-500 mr-1"></i> <span class="text-green-700 text-xl">${data.ward}</span>`;
            }
            
            // Scroll to result
            resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

    </script>
</body>
</html>
