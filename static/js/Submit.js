// 在全局添加冷却计时器喵~
let isCoolingDown = false;
let coolDownTimer = null;

document.getElementById("submit").addEventListener("click", sendData);
document.getElementById("question").addEventListener("keypress", function(e) {
    if (e.key === "Enter" && !isCoolingDown) sendData();
});

function sendData() {
    // 如果正在冷却就阻止喵！
    if(isCoolingDown) {
        console.log('喵喵哒~ 点击太快啦！(>^ω^<)');
        return;
    }
    
    const inputText = document.getElementById("question").value;
    const submitBtn = document.getElementById("submit");
    
    // 启动冷却并禁用按钮
    isCoolingDown = true;
    submitBtn.disabled = true;
    submitBtn.classList.add('disabled'); // 添加视觉反馈
    
    fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText })
    })
    .then(response => response.json())
    .then(data => {
        console.log('后端说:', data);
        // window.location.replace(data['url']);
    })
    .catch(error => {
        console.error('传输出错:', error);
    })
    .finally(() => {
        // 3秒冷却时间（可根据需要调整喵~）
        coolDownTimer = setTimeout(() => {
            isCoolingDown = false;
            submitBtn.disabled = false;
            submitBtn.classList.remove('disabled');
        }, 3000);
    });
}