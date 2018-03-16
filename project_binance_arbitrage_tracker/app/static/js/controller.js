$(document).ready(function() {
    table = $('#latestTablew').DataTable({
        "order": [
            [3, "desc"]
        ],
        "ajax": {
            "url": "/ajax-table/",
            "type": "POST"
        },
        "columns": [{
                "data": "token"
            },
            {
                "data": "BTC"
            },
            {
                "data": "BTC_EQUIV"
            },
            {
                "data": "ARBITRAGE"
            },
        ],
        'rowCallback': function(row, data, index) {
            if (data.ARBITRAGE > 0) {
                $(row).find('td:eq(3)').css('color', 'green');
            } else if (data.ARBITRAGE < 0) {
                $(row).find('td:eq(3)').css('color', 'red');
            } else {
                $(row).find('td:eq(3)').css('color', '#cfd2da');
            }
        }

    });

    setInterval(function() {
        table.ajax.reload();
    }, 10000);

});