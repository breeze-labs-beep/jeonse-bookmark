const fs = require('fs');

const urls = [
    "http://www.iros.go.kr/",
    "https://www.gov.kr/",
    "http://www.molit.go.kr/",
    "https://www.moj.go.kr/",
    "http://rt.molit.go.kr/",
    "https://kbland.kr/",
    "https://land.naver.com/",
    "https://hogangnono.com/",
    "https://www.khug.or.kr/",
    "https://www.hf.go.kr/",
    "https://www.sgic.co.kr/",
    "https://www.peterpanz.com/",
    "https://www.jsan.or.kr/"
];

const fetchMetadata = async (url) => {
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); // 5s timeout

        const response = await fetch(url, { 
            signal: controller.signal,
            headers: {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
        });
        clearTimeout(timeoutId);

        if (!response.ok) return { url, error: response.statusText };
        
        const html = await response.text();
        
        const getMeta = (prop) => {
            const match = html.match(new RegExp(`<meta\\s+(?:property|name)=["']${prop}["']\\s+content=["'](.*?)["']`, 'i'));
            return match ? match[1] : null;
        };

        return {
            url,
            title: getMeta('og:title') || getMeta('twitter:title'),
            description: getMeta('og:description') || getMeta('twitter:description'),
            image: getMeta('og:image') || getMeta('twitter:image')
        };
    } catch (e) {
        return { url, error: e.message };
    }
};

(async () => {
    const results = [];
    for (const url of urls) {
        console.log(`Fetching ${url}...`);
        const data = await fetchMetadata(url);
        results.push(data);
    }
    
    fs.writeFileSync('metadata.json', JSON.stringify(results, null, 2));
    console.log('Done! Saved to metadata.json');
})();
