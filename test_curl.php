<?php
// Test how curl handles just a hostname

$test_hosts = [
    "127.0.0.1",
    "localhost",
    "127.0.0.1:80",
    "localhost:80",
];

foreach ($test_hosts as $host) {
    echo "\n=== Testing curl with: $host ===\n";
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $host);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 2);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 2);
    
    $response = curl_exec($ch);
    
    if (curl_errno($ch)) {
        echo "Error: " . curl_error($ch) . "\n";
    } else {
        echo "Success! Response length: " . strlen($response) . "\n";
        echo "First 100 chars: " . substr($response, 0, 100) . "\n";
    }
    
    curl_close($ch);
}
?>
