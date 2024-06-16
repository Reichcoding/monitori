// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

myCharts = {}
function generate_chart(ctx_id,chart_data){
  if(window.myCharts[ctx_id] != undefined){
    window.myCharts[ctx_id].destroy()
    console.log('destroy chart')
  };
    window.myCharts[ctx_id] = new Chart(document.getElementById(ctx_id),{type: 'bar',
    data: { labels: chart_data.map(row => row.time),
        datasets: [{
            label: 'Нагрузка',
            data: chart_data.map(row => row.load),
            backgroundColor: "#4e73df",
            hoverBackgroundColor: "#2e59d9",
            borderColor: "#4e73df",
        }],},options:{legend: {display: false},
        scales: {
          responsive:true,
          xAxes: [{
            time: {
              unit: 'Время'
            },
            gridLines: {
              display: false,
              drawBorder: false
            },
            ticks: {
              maxTicksLimit: 12
            },
            maxBarThickness: 25,
          }],
          yAxes: [{
            ticks: {
              min: 0,
              max: 100,
              maxTicksLimit: 20,
              padding: 10,
              
              callback: function(value, index, values) {
                return number_format(value)+"%";
              }
            },
            gridLines: {
              color: "rgb(234, 236, 244)",
              zeroLineColor: "rgb(234, 236, 244)",
              drawBorder: false,
              borderDash: [2],
              zeroLineBorderDash: [2]
            }
          }],
        },
      }
    });
}

function generate_total_chart(ctx_id,cpu_data,ram_data,disk_data){
  if(window.myCharts[ctx_id] != undefined){
    window.myCharts[ctx_id].destroy()
    console.log('destroy chart')
  };
    window.myCharts[ctx_id] = new Chart(document.getElementById(ctx_id),{type: 'line',
    data: { labels: cpu_data.map(row => row.time),
        datasets: [{
          label: 'Нагрузка ЦПУ',
          data: cpu_data.map(row => row.load),
          borderColor: "red",
          backgroundColor: "rgba(255, 99, 132, 0)"
      },
      {
        label: 'Нагрузка ОЗУ',
        data: ram_data.map(row => row.load),
        borderColor: "green",
        backgroundColor: "rgba(255, 99, 132, 0)"
    },
    {
      label: 'Нагрузка диска',
      data: disk_data.map(row => row.load),
      borderColor: "blue",
      backgroundColor: "rgba(255, 99, 132, 0)"
  },
      ]},options:{legend: {display: true},
        scales: {
          responsive:true,
          xAxes: [{
            time: {
              unit: 'Время'
            },
            gridLines: {
              display: false,
              drawBorder: false
            },
            ticks: {
              maxTicksLimit: 12
            },
            maxBarThickness: 25,
          }],
          yAxes: [{
            ticks: {
              min: 0,
              max: 100,
              maxTicksLimit: 10,
              padding: 10,
              
              callback: function(value, index, values) {
                return number_format(value)+"%";
              }
            },
            gridLines: {
              color: "rgb(234, 236, 244)",
              zeroLineColor: "rgb(234, 236, 244)",
              drawBorder: false,
              borderDash: [2],
              zeroLineBorderDash: [2]
            }
          }],
        },
      }
    });
}
