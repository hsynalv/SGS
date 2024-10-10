document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('tool').addEventListener('change', function() {
        var selectedTool = this.value;

        var niktoOptions = document.getElementById('nikto-options');
        var nmapOptions = document.getElementById('nmap-options');
        var raccoonOptions = document.getElementById('raccoon-options');
        var skipfishOptions = document.getElementById('skipfish-options');
        var wapitiOptions = document.getElementById('wapiti-options');
        var dirbOptions = document.getElementById('dirb-options');
        var googleDorkOptions = document.getElementById('google-dork-options');
        var slowlorisOptions = document.getElementById('slowloris-options');
        var sublist3rOptions = document.getElementById('sublist3r-options');

        var toolOptions = [
            niktoOptions, nmapOptions, raccoonOptions, skipfishOptions, wapitiOptions,
            dirbOptions, googleDorkOptions, slowlorisOptions, sublist3rOptions
        ];

        // Tüm alanları gizle ve required özelliğini kaldır
        toolOptions.forEach(function(option) {
            if (option) {
                option.style.display = 'none';
                // Gizli form alanlarındaki inputlardan required niteliğini kaldır
                var inputs = option.querySelectorAll('input, select');
                inputs.forEach(function(input) {
                    input.removeAttribute('required');
                });
            }
        });

        // Seçilen aracı göster ve input alanlarına required ekle
        var selectedOptions;
        if (selectedTool === 'nikto') {
            selectedOptions = niktoOptions;
        } else if (selectedTool === 'nmap') {
            selectedOptions = nmapOptions;
        } else if (selectedTool === 'raccoon') {
            selectedOptions = raccoonOptions;
        } else if (selectedTool === 'skipfish') {
            selectedOptions = skipfishOptions;
        } else if (selectedTool === 'wapiti') {
            selectedOptions = wapitiOptions;
        } else if (selectedTool === 'dirb') {
            selectedOptions = dirbOptions;
        } else if (selectedTool === 'google_dork') {
            selectedOptions = googleDorkOptions;
        } else if (selectedTool === 'slowloris_ddos') {
            selectedOptions = slowlorisOptions;
        } else if (selectedTool === 'sublist3r') {
            selectedOptions = sublist3rOptions;
        }

        if (selectedOptions) {
            selectedOptions.style.display = 'block';
            var visibleInputs = selectedOptions.querySelectorAll('input, select');
            visibleInputs.forEach(function(input) {
                input.setAttribute('required', '');
            });
        }
    });
});


var socket = io.connect('http://' + document.domain + ':' + location.port, {
    reconnection: true,       // Yeniden bağlantıya izin ver
    reconnectionAttempts: 5,  // Yeniden bağlanma deneme sayısı
    reconnectionDelay: 1000,  // Yeniden bağlanma denemeleri arası süre
    timeout: 20000            // Maksimum bağlantı bekleme süresi (ms)
});
// WebSocket ile tarama durumunu dinliyoruz
socket.on('progress', function(data) {
    console.log(data); // Veriyi görmek için ekledik
    document.getElementById('status-text').innerText = data.status;
});
function startScan() {
    var tool = document.getElementById('tool').value;
    var data = {
        tool: tool,
        // Gerekli diğer form verilerini ekleyin
    };
    // Nikto aracı seçildiyse, ilgili alanların varlığını kontrol et
    // Nikto aracı seçildiyse
    if (tool === 'nikto') {
        var domainNikto = document.getElementById('domain-nikto');
        var portNikto = document.getElementById('port-nikto');
        var sslOptionNikto = document.getElementById('ssl_option');
        if (domainNikto && portNikto && sslOptionNikto) {
            data['domain'] = domainNikto.value;
            data['port'] = portNikto.value;
            data['ssl_option'] = sslOptionNikto.value;
        } else {
            console.error("Nikto form alanları bulunamadı.");
        }
    }
    // Nmap aracı seçildiyse
    if (tool === 'nmap') {
        var domainNmap = document.getElementById('domain-nmap');
        var scanTypeNmap = document.getElementById('scan_type');
        if (domainNmap && scanTypeNmap) {
            data['domain'] = domainNmap.value;
            data['scan_type'] = scanTypeNmap.value;
        } else {
            console.error("Nmap form alanları bulunamadı.");
        }
    }
    // Wapiti aracı seçildiyse
    if (tool === 'wapiti') {
        var urlWapiti = document.getElementById('url-wapiti');
        if (urlWapiti) {
            data['url'] = urlWapiti.value;
        } else {
            console.error("Wapiti form alanı bulunamadı.");
        }
    }
    // Skipfish aracı seçildiyse
    if (tool === 'skipfish') {
        var urlSkipfish = document.getElementById('url-skipfish');
        if (urlSkipfish) {
            data['url'] = urlSkipfish.value;
        } else {
            console.error("Skipfish form alanı bulunamadı.");
        }
    }
    // Dirb aracı seçildiyse
    if (tool === 'dirb') {
        var urlDirb = document.getElementById('url-dirb');
        if (urlDirb) {
            data['url'] = urlDirb.value;
        } else {
            console.error("Dirb form alanı bulunamadı.");
        }
    }
    // Google Dork aracı seçildiyse
    if (tool === 'google_dork') {
        var domainGoogle = document.getElementById('domain-google');
        if (domainGoogle) {
            data['domain'] = domainGoogle.value;
        } else {
            console.error("Google Dork form alanı bulunamadı.");
        }
    }
    // Slowloris DDOS aracı seçildiyse
    if (tool === 'slowloris_ddos') {
        var urlSlowloris = document.getElementById('url-slowloris');
        if (urlSlowloris) {
            data['url'] = urlSlowloris.value;
        } else {
            console.error("Slowloris form alanı bulunamadı.");
        }
    }
    // Sublist3r aracı seçildiyse
    if (tool === 'sublist3r') {
        var domainSublist3r = document.getElementById('domain-sublist3r');
        if (domainSublist3r) {
            data['domain'] = domainSublist3r.value;
        } else {
            console.error("Sublist3r form alanı bulunamadı.");
        }
    }
    // Raccoon aracı seçildiyse
    if (tool === 'raccoon') {
        var domainRaccoon = document.getElementById('domain-raccoon');
        if (domainRaccoon) {
            data['domain'] = domainRaccoon.value;
        } else {
            console.error("Raccon form alanı bulunamadı.");
        }
    }
    console.log(data)
    socket.emit('start_scan', data);

    // Yönlendirme tarama durumu sayfasına
    window.location.href = '/scan_status';
}