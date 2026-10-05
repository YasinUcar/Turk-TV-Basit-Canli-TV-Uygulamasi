const path = require('path');
const { app, BrowserWindow, session, Menu } = require('electron');
app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');
function create() {
  Menu.setApplicationMenu(null);
  const win = new BrowserWindow({ width: 1280, height: 760, title: 'Türk TV', icon: path.join(__dirname, 'icon.png'), backgroundColor: '#111', autoHideMenuBar: true });
  session.defaultSession.webRequest.onHeadersReceived((d, cb) => {
    const h = d.responseHeaders || {};
    for (const k of Object.keys(h)) if (k.toLowerCase().startsWith('access-control-')) delete h[k];
    h['Access-Control-Allow-Origin'] = ['*'];
    h['Access-Control-Allow-Headers'] = ['*'];
    h['Access-Control-Allow-Methods'] = ['GET, OPTIONS'];
    cb({ responseHeaders: h });
  });
  win.loadFile('index.html');
  win.maximize();
}
app.whenReady().then(create);
app.on('window-all-closed', () => app.quit());
