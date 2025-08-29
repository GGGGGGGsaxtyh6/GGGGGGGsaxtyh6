// Script de Frida para interceptar funciones de escritura de archivos
console.log("[*] Script cargado. Interceptando funciones de escritura...");

// Interceptar WriteFile
try {
    var writeFile = Module.findExportByName("kernel32.dll", "WriteFile");
    if (writeFile) {
        Interceptor.attach(writeFile, {
            onEnter: function(args) {
                console.log("[+] WriteFile llamado!");
                console.log("    Handle: " + args[0]);
                console.log("    Buffer: " + args[1]);
                console.log("    Size: " + args[2]);
                
                // Leer el contenido del buffer
                try {
                    var buffer = Memory.readUtf8String(args[1], args[2].toInt32());
                    console.log("    Contenido: " + buffer);
                } catch (e) {
                    try {
                        var buffer = Memory.readByteArray(args[1], Math.min(args[2].toInt32(), 200));
                        console.log("    Contenido (hex): " + hexdump(buffer));
                    } catch (e2) {
                        console.log("    No se pudo leer el contenido");
                    }
                }
            },
            onLeave: function(retval) {
                console.log("[+] WriteFile retornó: " + retval);
            }
        });
        console.log("[*] WriteFile interceptado exitosamente");
    }
} catch (e) {
    console.log("[-] Error interceptando WriteFile: " + e);
}

// Interceptar CreateFileA
try {
    var createFileA = Module.findExportByName("kernel32.dll", "CreateFileA");
    if (createFileA) {
        Interceptor.attach(createFileA, {
            onEnter: function(args) {
                var filename = Memory.readUtf8String(args[0]);
                console.log("[+] CreateFileA llamado: " + filename);
            }
        });
        console.log("[*] CreateFileA interceptado exitosamente");
    }
} catch (e) {
    console.log("[-] Error interceptando CreateFileA: " + e);
}

// Interceptar CreateFileW
try {
    var createFileW = Module.findExportByName("kernel32.dll", "CreateFileW");
    if (createFileW) {
        Interceptor.attach(createFileW, {
            onEnter: function(args) {
                var filename = Memory.readUtf16String(args[0]);
                console.log("[+] CreateFileW llamado: " + filename);
            }
        });
        console.log("[*] CreateFileW interceptado exitosamente");
    }
} catch (e) {
    console.log("[-] Error interceptando CreateFileW: " + e);
}

console.log("[*] Script de interceptación listo. Esperando llamadas...");