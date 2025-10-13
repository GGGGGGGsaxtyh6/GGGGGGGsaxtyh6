const fs = require('fs');
const vm = require('vm');

const inline = fs.readFileSync('/workspace/target/inline.js','utf8');

const functionBodies = [];
const alerts = [];
const scheduled = [];
let lastLocation = '';

// Create a minimal DOM stub
let onsubmitFn = null;
const usernameEl = { value: '', placeholder: 'USERNAME' };
const passwordEl = { value: '', placeholder: 'PASSWORD' };
const formEl = {};
Object.defineProperty(formEl, 'onsubmit', {
  set(fn) { onsubmitFn = fn; },
  get() { return onsubmitFn; }
});

const locationStub = {
  set href(v) { lastLocation = String(v); },
  get href() { return lastLocation; }
};

const documentStub = {
  location: locationStub,
  getElementById(id) {
    if (id === 'login') return formEl;
    if (id === 'username') return usernameEl;
    if (id === 'password') return passwordEl;
    return {};
  }
};

const context = {
  console,
  window: {},
  document: documentStub,
  location: locationStub,
  alert: (msg) => { alerts.push(String(msg)); },
  setTimeout: (fn, t) => {
    if (typeof fn === 'string') { scheduled.push({ type: 'string', code: String(fn) }); }
    else if (typeof fn === 'function') { try { fn(); } catch (e) {} }
  },
  setInterval: (fn, t) => { /* ignore */ },
};

// Expose window to refer to global
context.window = context;

const sandbox = vm.createContext(context);

// Preload hooks inside the sandbox to intercept Function constructor via both global and property access
const prelude = `
  (function(){
    const __functionBodies = [];
    const OriginalFunction = Function;
    function InterceptedFunction(){
      const args = Array.prototype.slice.call(arguments);
      const body = args.length ? String(args[args.length - 1]) : '';
      __functionBodies.push(body);
      return OriginalFunction.apply(this, args);
    }
    // Expose for host to read
    this.__getCapturedBodies = function(){ return __functionBodies.slice(); };
    // Replace global Function
    this.Function = InterceptedFunction;
    // Replace constructor getter for all function objects
    Object.defineProperty(Function.prototype, 'constructor', {
      configurable: true,
      enumerable: false,
      get: function(){ return InterceptedFunction; }
    });
    // Hook eval as well, if used
    const __origEval = this.eval;
    this.eval = function(code){
      try { __functionBodies.push(String(code)); } catch(e) {}
      return __origEval.call(this, code);
    };
  })();
`;

vm.runInContext(prelude, sandbox, { timeout: 5000 });

// Run the inline script to set up handlers
vm.runInContext(inline, sandbox, { timeout: 5000 });

if (typeof sandbox.window.onload === 'function') {
  sandbox.window.onload();
}

// Log whether onsubmit was set
console.log('Has onsubmit:', typeof onsubmitFn);
try { fs.writeFileSync('/workspace/target/onsubmit_tostring.txt', String(onsubmitFn)); } catch (e) {}

// Try a first submit with empty values (should fail, but triggers code paths)
usernameEl.value = '';
passwordEl.value = '';
if (typeof onsubmitFn === 'function') {
  try { onsubmitFn(); } catch (e) {}
}

// Capture bodies
try {
  const bodies = sandbox.__getCapturedBodies ? sandbox.__getCapturedBodies() : [];
  functionBodies.push.apply(functionBodies, bodies);
} catch (e) {}

// Execute any scheduled string code (from setTimeout with string)
for (let i = 0; i < scheduled.length; i++) {
  const item = scheduled[i];
  if (item.type === 'string') {
    try {
      functionBodies.push(item.code);
      vm.runInContext(item.code, sandbox, { timeout: 5000 });
    } catch (e) {}
  }
}

// Save captured function bodies and alerts
fs.writeFileSync('/workspace/target/functions.log', functionBodies.join('\n\n/* --- NEXT FUNCTION --- */\n\n'));
fs.writeFileSync('/workspace/target/alerts.log', alerts.join('\n'));
fs.writeFileSync('/workspace/target/location.log', lastLocation);

// Try to heuristically find a likely credential check in captured functions
const interesting = functionBodies.filter(b => /username|password|getElementById\(['\"]username|getElementById\(['\"]password|247CTF|flag/i.test(b));
fs.writeFileSync('/workspace/target/interesting.log', interesting.join('\n\n/* --- NEXT INTERESTING --- */\n\n'));

console.log('Captured functions:', functionBodies.length);
console.log('Alerts captured:', alerts.length);
console.log('Location set to:', lastLocation);

// Try a few guesses for username/password
const guesses = [
  ['admin','admin'],
  ['admin','password'],
  ['administrator','administrator'],
  ['administrator','password'],
  ['admin','letmein'],
  ['root','root'],
  ['ctf','ctf'],
  ['user','user'],
  ['guest','guest'],
  ['admin','247ctf'],
  ['admin','247CTF'],
  ['admin','flag'],
  ['admin','supersecret'],
];

for (const [u,p] of guesses) {
  lastLocation = '';
  alerts.length = 0;
  usernameEl.value = u;
  passwordEl.value = p;
  if (typeof onsubmitFn === 'function') {
    try { onsubmitFn(); } catch (e) {}
  }
  if (lastLocation || alerts.length) {
    fs.writeFileSync('/workspace/target/success.json', JSON.stringify({u,p,lastLocation,alerts}, null, 2));
    console.log('Found reaction for', u, p, '->', lastLocation, alerts[0]||'');
    break;
  }
}
