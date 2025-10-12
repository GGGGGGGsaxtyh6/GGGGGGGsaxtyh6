<?php
// Test more advanced URL bypasses

$test_urls = [
    // CRLF injection attempts
    "http://motherland.com%0d%0a/",
    "http://motherland.com%0a/",
    "http://motherland.com%0d/",
    
    // Null byte
    "http://motherland.com%00/",
    "http://motherland.com\x00/",
    
    // Unicode/encoding tricks
    "http://motherland.com%2f/",
    "http://motherland.com%2e/",
    
    // Fragment tricks  
    "http://motherland.com#@127.0.0.1",
    "http://motherland.com/#127.0.0.1",
    
    // Double encoding
    "http://motherland.com%252f/",
    
    // IPv6
    "http://[::1].motherland.com/",
    "http://[0:0:0:0:0:0:0:1].motherland.com/",
    
    // Other tricks
    "http://motherland.com;@127.0.0.1/",
    "http://motherland.com:.80/",
    "http://motherland.com:0/",
    "http://motherland.com:/",
    
    // Path traversal in hostname?
    "http://127.0.0.1/../motherland.com/",
    "http://127.0.0.1/..;/motherland.com/",
];

foreach ($test_urls as $url) {
    echo "\n=== Testing: $url ===\n";
    
    if(filter_var($url, FILTER_VALIDATE_URL)) {
        $parsedUrl = parse_url($url);
        echo "Valid URL\n";
        echo "Host: " . ($parsedUrl['host'] ?? 'NULL') . "\n";
        
        if(isset($parsedUrl['host']) && preg_match('/motherland\.com$/', $parsedUrl['host'])) {
            echo "✓ Regex matches!\n";
            echo "CURLOPT_URL would be: " . $parsedUrl['host'] . "\n";
            
            // Check if it looks interesting
            if (strpos($parsedUrl['host'], '127.0.0.1') !== false || 
                strpos($parsedUrl['host'], 'localhost') !== false ||
                strpos($parsedUrl['host'], '::1') !== false) {
                echo "*** INTERESTING! Contains localhost reference! ***\n";
            }
        } else {
            echo "✗ Regex doesn't match\n";
            if (isset($parsedUrl['host'])) {
                echo "   Host value: {$parsedUrl['host']}\n";
            }
        }
    } else {
        echo "Invalid URL (filter_var failed)\n";
    }
}
?>
