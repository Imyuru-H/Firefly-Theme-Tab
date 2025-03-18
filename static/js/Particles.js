!(function () {
	function n(n, e, t) {
		return n.getAttribute(e) || t;
	}

	function e(n) {
		return document.getElementsByTagName(n);
	}

	function f(n) {
		return document.getElementById(n);
	}

	function t() {
		var t = e("script"),
			o = t.length,
			i = t[o - 1];
		return {
			l: o,
			z: n(i, "zIndex", 0),
			o: n(i, "opacity", 0.6),
			c: n(i, "color", "0,255,0"),
			n: n(i, "count", 512), // 粒子的数量
		};
	}

	function o() {
		(a = m.width =
			window.innerWidth ||
			document.documentElement.clientWidth ||
			document.body.clientWidth),
			(c = m.height =
				window.innerHeight ||
				document.documentElement.clientHeight ||
				document.body.clientHeight);
	}

	function i() {
		r.clearRect(0, 0, a, c);
		var n, e, t, o, m, l;

		s.forEach(function (particle, index) {
			for (
				particle.x += particle.xa,
				particle.y += particle.ya,
				particle.xa *= particle.x > a || particle.x < 0 ? -1 : 1,
				particle.ya *= particle.y > c || particle.y < 0 ? -1 : 1,
				// 使用粒子的颜色属性进行绘制
				r.fillStyle = particle.color,
				r.fillRect(particle.x - 0.5, particle.y - 0.5, 1, 1),
				e = index + 1;
				e < u.length;
				e++
			) {
				(n = u[e]),
					null !== n.x &&
					null !== n.y &&
					((o = particle.x - n.x),
						(m = particle.y - n.y),
						(l = o * o + m * m),
						l < n.max &&
						(n === y &&
							l >= n.max / 2 &&
							((particle.x -= 0.03 * o), (particle.y -= 0.03 * m)),
							(t = (n.max - l) / n.max),
							r.beginPath(),
							(r.lineWidth = t / 2),
							// 连线颜色和粒子颜色一致
							r.strokeStyle = particle.color,
							r.moveTo(particle.x, particle.y),
							r.lineTo(n.x, n.y),
							r.stroke()));
			}
		}),
			x(i);
	}

	// 定义颜色
	var fixedColors = [
		"rgba(255, 0, 0, 1.0)",   // 红色
		"rgba(0, 255, 0, 1.0)",   // 绿色
		"rgba(0, 0, 255, 1.0)",   // 蓝色
		"rgba(255, 255, 0, 1.0)", // 黄色
		"rgba(0, 255, 255, 0.8)", // 青色
		"rgba(255, 0, 255, 0.8)", // 紫色
		"rgba(255, 165, 0, 0.8)", // 橙色
		"rgba(127, 255, 212, 1.0)",
		"rgba(0, 255, 127, 1.0)"];
	
	// 定义DOM变量
	var a,
		c,
		u,
		m = document.createElement("canvas"),
		d = t(),
		l = "c_n" + d.l,
		r = m.getContext("2d"),
		x =
			window.requestAnimationFrame ||
			window.webkitRequestAnimationFrame ||
			window.mozRequestAnimationFrame ||
			window.oRequestAnimationFrame ||
			window.msRequestAnimationFrame ||
			function (n) {
				window.setTimeout(n, 1e3 / 45);
			},
		w = Math.random,
		y = { x: null, y: null, max: 2e4 };
	(m.id = l),
		(m.style.cssText =
			"position:fixed;top:0;left:0;z-index:" + d.z + ";opacity:" + d.o),
		f("particle").appendChild(m),
		o(),
		(window.onresize = o),
		(window.onmousemove = function (n) {
			(n = n || window.event), (y.x = n.clientX), (y.y = n.clientY);
		}),
		(window.onmouseout = function () {
			(y.x = null), (y.y = null);
		});

	//固定颜色
	for (var s = [], f = 0; d.n > f; f++) {
		var h = w() * a,
			g = w() * c,
			v = 2 * w() - 1,
			p = 2 * w() - 1,
			// 从固定颜色数组中随机选择一个颜色
			color = fixedColors[Math.floor(Math.random() * fixedColors.length)];
		
		s.push({ x: h, y: g, xa: v, ya: p, max: 6e3, color: color }); // 使用选定的固定颜色
	}

	(u = s.concat([y])),
		setTimeout(function () {
			i();
		}, 100);
})();