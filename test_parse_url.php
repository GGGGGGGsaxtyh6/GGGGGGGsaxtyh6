<?php
// Test various URL parsing techniques to find bypasses

$test_urls = [
    "http://motherland.com/",
    "http://127.0.0.1.motherland.com/",
    "http://motherland.com@127.0.0.1/",
    "http://127.0.0.1@motherland.com/",
    "http://motherland.com#127.0.0.1",
    "http://motherland.com:80/path",
    "http://motherland.com%20127.0.0.1/",
    "http://motherland.com%2F127.0.0.1/",
    "http://motherland.com/../127.0.0.1/",
    "http://localhost.motherland.com/",
    "http://0x7f000001.motherland.com/",
    "http://2130706433.motherland.com/",
    "http://motherland.com\\@127.0.0.1/",
    "http://motherland.com/index.php",
    "http://motherland.com:80",
    "http://user:pass@motherland.com/",
];

foreach ($test_urls as $url) {
    echo "\n=== Testing: $url ===\n";
    
    if(filter_var($url, FILTER_VALIDATE_URL)) {
        $parsedUrl = parse_url($url);
        echo "Valid URL\n";
        echo "Host: " . ($parsedUrl['host'] ?? 'NULL') . "\n";
        echo "Port: " . ($parsedUrl['port'] ?? 'NULL') . "\n";
        echo "Path: " . ($parsedUrl['path'] ?? 'NULL') . "\n";
        echo "User: " . ($parsedUrl['user'] ?? 'NULL') . "\n";
        
        // Check regex
        if(isset($parsedUrl['host']) && preg_match('/motherland\.com$/', $parsedUrl['host'])) {
            echo "✓ Regex matches!\n";
            echo "CURLOPT_URL would be set to: " . $parsedUrl['host'] . "\n";
        } else {
            echo "✗ Regex doesn't match\n";
        }
    } else {
        echo "Invalid URL\n";
    }
}
?>
