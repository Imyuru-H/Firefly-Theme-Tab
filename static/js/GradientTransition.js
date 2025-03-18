document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.getElementById("submit");
    const inputContainer = document.getElementById("input");
    let animationFrame;
    let startTime;

    // HSL颜色格式解析器
    const parseHSL = (hslStr) => {
        const regex = /hsl\((\d+\.?\d*),\s*(\d+\.?\d*)%?,\s*(\d+\.?\d*)%?\)/;
        const match = hslStr.match(regex);
        return match ? match.slice(1,4).map(Number) : null;
    };

    // 动画配置参数
    const config = {
        duration: 100,
        bezier: [0.25, 0.1, 0.25, 1],
        startColor: "hsl(0, 0%, 29%)",
        targetGradient: [ 
            { pos: "0%", color: "hsl(0, 0%, 29%)" },
            { pos: "18.5%", color: "hsl(171.78, 0.01%, 29.02%)" },
            { pos: "34.2%", color: "hsl(171.78, 0.12%, 29.12%)" },
            { pos: "47.4%", color: "hsl(171.78, 0.39%, 29.42%)" },
            { pos: "58.2%", color: "hsl(171.78, 0.91%, 29.99%)" },
            { pos: "60%", color: "hsl(171.78, 1.71%, 30.93%)" },
            { pos: "74.1%", color: "hsl(171.78, 2.83%, 32.33%)" },
            { pos: "79.6%", color: "hsl(171.78, 4.24%, 34.28%)" },
            { pos: "83.9%", color: "hsl(171.78, 5.89%, 36.89%)" },
            { pos: "87.1%", color: "hsl(171.78, 7.69%, 40.23%)" },
            { pos: "89.6%", color: "hsl(171.78, 9.55%, 44.4%)" },
            { pos: "91.7%", color: "hsl(171.78, 11.4%, 49.5%)" },
            { pos: "93.4%", color: "hsl(171.78, 16.51%, 55.61%)" },
            { pos: "95.3%", color: "hsl(171.78, 25.07%, 62.84%)" },
            { pos: "97.4%", color: "hsl(171.78, 40.5%, 71.26%)" },
            { pos: "100%", color: "hsl(171.78, 75.26%, 80.98%)" }
        ]
    };

    // 初始化颜色数据
    config.targetGradient = config.targetGradient.map(stop => ({
        pos: stop.pos,
        hsl: parseHSL(stop.color)
    }));
    const startHSL = parseHSL(config.startColor);

    // 贝塞尔曲线计算
    const cubicBezier = (t, p1, p2, p3, p4) => {
        const ct = 1 - t;
        return 3 * ct * ct * t * p2 + 3 * ct * t * t * p3 + t * t * t * p4;
    };

    // 动画核心逻辑
    const animate = (timestamp) => {
        if (!startTime) startTime = timestamp;
        const elapsed = timestamp - startTime;
        const progress = Math.min(elapsed / config.duration, 1);
        
        const easedProgress = cubicBezier(
            progress,
            ...config.bezier
        );

        const gradientStops = config.targetGradient.map(stop => {
            const [h, s, l] = stop.hsl.map((val, i) => 
                startHSL[i] + (val - startHSL[i]) * easedProgress
            );
            return `hsl(${h}, ${s}%, ${l}%) ${stop.pos}`;
        });

        inputContainer.style.background = 
            `linear-gradient(to right, ${gradientStops.join(", ")})`;

        progress < 1 && (animationFrame = requestAnimationFrame(animate));
    };

    // 事件绑定
    submitBtn.addEventListener("mouseenter", () => {
        cancelAnimationFrame(animationFrame);
        startTime = null;
        animationFrame = requestAnimationFrame(animate);
    });

    submitBtn.addEventListener("mouseleave", () => {
        // 立即终止动画
    cancelAnimationFrame(animationFrame);
    animationFrame = null;

    // 同步操作：禁用过渡 → 设置颜色 → 强制渲染 → 恢复过渡
    inputContainer.style.transition = 'none';
    inputContainer.style.background = config.startColor;
    
    // 强制浏览器同步渲染
    void inputContainer.offsetHeight; // 触发重绘
    
    // 下一帧恢复原有过渡
    requestAnimationFrame(() => {
        inputContainer.style.transition = '';
    });
    });
})