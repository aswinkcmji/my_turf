(function (jQuery) {
  "use strict";
if (document.querySelectorAll('#matchChart').length) {
  var options = {
    series: [total_completed_matches,total_cancelled_matches],
    labels: [`Completed Matches-${total_completed_matches}`,`Cancelled Matches-${total_cancelled_matches}`],
    chart: {
    type: 'donut',
    height:'250px',
   
    plotOptions: {
      pie: {
        // customScale: 10 ,
        donut: {
          // size: '10%'
        }
      }
    },
  },
  responsive: [{
    breakpoint: 100,
    options: {
      legend: {
        position: 'bottom'
      }
    }
  }]
  };

  // var chart = new ApexCharts(document.querySelector("#chart"), options);
  // chart.render();
  if(ApexCharts !== undefined) {
    const chart = new ApexCharts(document.querySelector("#matchChart"), options);
    chart.render();
    document.addEventListener('ColorChange', (e) => {
        const newOpt = {colors: [e.detail.detail1, e.detail.detail2],}
        chart.updateOptions(newOpt)
       
    })
  }
}
if (document.querySelectorAll('#d-activity').length) {
    const options = {
      series: [{
        name: '',
        data: categories_in_matches
      }, {
        // name: 'Failed deals',
        // data: [40, 50, 55, 50, 30, 80, 30, 40, 50, 55]
      }],
      chart: {
        type: 'bar',
        height: 230,
        stacked: true,
        toolbar: {
            show:false
          }
      },
      colors: ["#3a57e8", "#4bc7d2"],
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '28%',
          // endingShape: 'rounded',
          //  
        },
      },
      legend: {
        show: false
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
      },
      xaxis: {
        categories:categories_list_in_js,
        labels: {
          minHeight:20,
          maxHeight:20,
          style: {
            colors: "#8A92A6",
          },
        }
      },
        yaxis: {
        title: {
          text: 'Number of matches created'
        },
        labels: {
            minWidth: 19,
            maxWidth: 19,
            style: {
              colors: "#8A92A6",
            },
        }
      },
      fill: {
        opacity: 1
      },
      tooltip: {
        y: {
          formatter: function (val) {
            return val + " Matches"
          }
        }
      }
    };
  
    const chart = new ApexCharts(document.querySelector("#d-activity"), options);
    chart.render();
    document.addEventListener('ColorChange', (e) => {
    const newOpt = {colors: [e.detail.detail1, e.detail.detail2],}
    chart.updateOptions(newOpt)
    })
  }
  if (document.querySelectorAll('#tournamentChart').length) {
    var options = {
      series: [total_completed_tournaments,total_cancelled_tournaments],
      labels: [`Completed Tournaments-${total_completed_tournaments}`,`Cancelled Tournaments-${total_cancelled_tournaments}`],
      chart: {
      type: 'donut',
      height:'250px',
     
      plotOptions: {
        pie: {
          // customScale: 10 ,
          donut: {
            // size: '10%'
          }
        }
      },
    },
    responsive: [{
      breakpoint: 100,
      options: {
        legend: {
          position: 'bottom'
        }
      }
    }]
    };
  
    // var chart = new ApexCharts(document.querySelector("#chart"), options);
    // chart.render();
    if(ApexCharts !== undefined) {
      const chart = new ApexCharts(document.querySelector("#tournamentChart"), options);
      chart.render();
      document.addEventListener('ColorChange', (e) => {
          const newOpt = {colors: [e.detail.detail1, e.detail.detail2],}
          chart.updateOptions(newOpt)
         
      })
    }
  }
  if (document.querySelectorAll('#d-activity-tournament').length) {
      const options = {
        series: [{
          name: '',
          data: categories_in_tournaments
        }, {
          // name: 'Failed deals',
          // data: [40, 50, 55, 50, 30, 80, 30, 40, 50, 55]
        }],
        chart: {
          type: 'bar',
          height: 230,
          stacked: true,
          toolbar: {
              show:false
            }
        },
        colors: ["#3a57e8", "#4bc7d2"],
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: '28%',
            // endingShape: 'rounded',
            //  
          },
        },
        legend: {
          show: false
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          show: true,
          width: 2,
          colors: ['transparent']
        },
        xaxis: {
          categories:categories_list_in_js,
          labels: {
            minHeight:20,
            maxHeight:20,
            style: {
              colors: "#8A92A6",
            },
          }
        },
          yaxis: {
          title: {
            text: 'Number of matches created'
          },
          labels: {
              minWidth: 19,
              maxWidth: 19,
              style: {
                colors: "#8A92A6",
              },
          }
        },
        fill: {
          opacity: 1
        },
        tooltip: {
          y: {
            formatter: function (val) {
              return val + " Matches"
            }
          }
        }
      };
    
      const chart = new ApexCharts(document.querySelector("#d-activity-tournament"), options);
      chart.render();
      document.addEventListener('ColorChange', (e) => {
      const newOpt = {colors: [e.detail.detail1, e.detail.detail2],}
      chart.updateOptions(newOpt)
      })
    }
if (document.querySelectorAll('#d-main').length) {
  const options = {
      series: [{  
          name: 'total',
          data: price_list
      }
      // , {
      //     name: 'pipline',
      //     data: [72, 60, 84, 60, 74, 60, 78]
      // }
    ],
    chart: {
      fontFamily: '"Inter", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"',
      height: 245,
      type: 'area',
      toolbar: {
          show: true
      },
      sparkline: {
          enabled: false,
      },
      zoom:{
        enabled: true,
      },
  },
  colors: ["#3a57e8", "#4bc7d2"],
  dataLabels: {
      enabled: false
  },
  stroke: {
      curve: 'smooth',
      width: 3,
  },
  yaxis: {
    show: true,
    labels: {
      show: true,
      minWidth: 19,
      maxWidth: 19,
      style: {
        colors: "#8A92A6",
      },
      offsetX: 10,
    },
    lines: {
      show: true  //or just here to disable only x axis grids
  }
  },
  legend: {
      show: false,
  },
  xaxis: {
      labels: {
          // minHeight:22,
          // maxHeight:22,
          show: false,
          // style: {
          //   colors: "#8A92A6",
          // },
      },
      lines: {
        show: true   //or just here to disable only x axis grids
      },
      categories:date_list
  },
      grid: {
          show: false,
      },
      // fill: {
      //     type: 'gradient',
      //     gradient: {
      //         shade: 'dark',
      //         type: "vertical",
      //         shadeIntensity: 0,
      //         gradientToColors: undefined, // optional, if not defined - uses the shades of same color in series
      //         inverseColors: true,
      //         opacityFrom: .4,
      //         opacityTo: .1,
      //         stops: [0, 50, 80],
      //         colors: ["#3a57e8", "#4bc7d2"]
      //     }
      // },
      tooltip: {
        enabled: true,
      },
  };

  const chart = new ApexCharts(document.querySelector("#d-main"), options);
  chart.render();
  // document.addEventListener('ColorChange', (e) => {
  //   console.log(e)
  //   const newOpt = {
  //     colors: [e.detail.detail1, e.detail.detail2],
  //     fill: {
  //       type: 'gradient',
  //       gradient: {
  //           shade: 'dark',
  //           type: "vertical",
  //           shadeIntensity: 0,
  //           gradientToColors: [e.detail.detail1, e.detail.detail2], // optional, if not defined - uses the shades of same color in series
  //           inverseColors: true,
  //           opacityFrom: .4,
  //           opacityTo: .1,
  //           stops: [0, 50, 60],
  //           colors: [e.detail.detail1, e.detail.detail2],
  //       }
  //   },
  //  }
  //   chart.updateOptions(newOpt)
  // })
}
if ($('.d-slider1').length > 0) {
    const options = {
        centeredSlides: false,
        loop: false,
        slidesPerView: 4,
        autoplay:false,
        spaceBetween: 32,
        breakpoints: {
            320: { slidesPerView: 1 },
            550: { slidesPerView: 2 },
            991: { slidesPerView: 3 },
            1400: { slidesPerView: 3 },
            1500: { slidesPerView: 4 },
            1920: { slidesPerView: 6 },
            2040: { slidesPerView: 7 },
            2440: { slidesPerView: 8 }
        },
        pagination: {
            el: '.swiper-pagination'
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
        },  

        // And if we need scrollbar
        scrollbar: {
            el: '.swiper-scrollbar'  
        }
    } 
    let swiper = new Swiper('.d-slider1',options);

    document.addEventListener('ChangeMode', (e) => {
      if (e.detail.rtl === 'rtl' || e.detail.rtl === 'ltr') {
        swiper.destroy(true, true)
        setTimeout(() => {
            swiper = new Swiper('.d-slider1',options);
        }, 500);
      }
    })
}

})(jQuery)
