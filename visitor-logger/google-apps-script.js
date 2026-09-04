// Google Apps Script — paste this into script.google.com
// Linked to your Google Sheet. See SETUP.md for instructions.

function doGet(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Timestamp', 'IP Address', 'Country', 'City', 'Page', 'Referrer', 'User Agent']);
      sheet.getRange(1, 1, 1, 7).setFontWeight('bold');
    }

    sheet.appendRow([
      e.parameter.ts      || new Date().toISOString(),
      e.parameter.ip      || 'unknown',
      e.parameter.country || '',
      e.parameter.city    || '',
      e.parameter.page    || '/',
      e.parameter.ref     || '',
      e.parameter.ua      || ''
    ]);
  } catch (err) {
    Logger.log('Error: ' + err.message);
  }

  return ContentService.createTextOutput('ok');
}

function doPost(e) {
  try {
    var data  = JSON.parse(e.postData.contents);
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Timestamp', 'IP Address', 'Country', 'City', 'Page', 'Referrer', 'User Agent']);
      sheet.getRange(1, 1, 1, 7).setFontWeight('bold');
    }

    sheet.appendRow([
      data.timestamp,
      data.ip,
      data.country,
      data.city,
      data.page,
      data.ref,
      data.ua,
    ]);
  } catch (err) {
    Logger.log('Error: ' + err.message);
  }

  return ContentService.createTextOutput('ok');
}

// Optional: test this function manually in the Apps Script editor
function testLog() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['Timestamp', 'IP Address', 'Country', 'City', 'Page', 'Referrer', 'User Agent']);
    sheet.getRange(1, 1, 1, 7).setFontWeight('bold');
  }
  sheet.appendRow([new Date().toISOString(), '123.45.67.89', 'US', 'New York', '/index.html', '', 'Test']);
}
