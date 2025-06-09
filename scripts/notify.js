function onEdit(e) {
  var sheet = e.source.getActiveSheet();
  var range = e.range;
  var row = range.getRow();
  var column = range.getColumn();

  if (sheet.getName() === "Sheet1" && column === 5 && range.getValue() === "Paid") {
    var telegramId = sheet.getValue(row, 1);
    var wallet = sheet.getValue(row, 2);
    var amount = sheet.getValue(row, 3);
    var processedAt = sheet.getValue(row, 6);

    var message = `🎉 *Withdrawal Processed*\n\n` +
                  `Wallet: ${wallet}\n` +
                  `Amount: ${amount} JHOOM Points\n` +
                  `Processed: ${processedAt}\n\n` +
                  `Thank you for participating in the JHOOM Airdrop!`;

    var url = `https://api.telegram.org/bot${YOUR_NOTIFY_BOT_TOKEN}/sendMessage`;
    var payload = {
      chat_id: telegramId,
      text: message,
      parse_mode: "Markdown"
    };

    var options = {
      method: "POST",
      contentType: "application/json",
      payload: JSON.stringify(payload)
    };

    UrlFetchApp.fetch(url, options);
  }
}
