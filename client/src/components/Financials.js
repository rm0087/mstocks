import React, { useEffect, useState } from "react";
import { Bar, Line } from 'react-chartjs-2';
// import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, PointElement } from 'chart.js';
import 'chart.js/auto'

// facts["us-gaap"].CashAndCashEquivalentsAtCarryingValue.units
export default function Financials({company}){
    
    let assetsData, liabilitiesData, stockholdersData, revenueData,revenueLabels, cashData, opCfData, opCfLabels, invCfData, invCfLabels, finCfData, finCfLabels, netCfData, netCfLabels, goodwillData, goodwillLabels, netIncomeData, netIncomeLabels; // declare chart/bar data
    let assetsLabels, primaryLabels; // declare chart/bar labels

    // const[api, setApi] = useState([])
    // const[incApi, setIncApi] = useState([])
    // const[cfApi, setCfApi] = useState([])

    // useEffect(() =>{

    //     // FUNCTIONS BEGIN ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //     const fetchBs = async () => {
    //         try {
    //             const response = await fetch(`/balance_sheets/${company.cik}`);
    //             if (response.ok) {
    //                 const data = await response.json();
    //                 setApi(data)
    //             } else {
    //                 setApi([])
    //                 console.error('Failed to fetch balance sheets:', response.status);
    //             }
    //         } catch (error) {
    //             console.error('Error fetching balance sheets:', error);
    //         }
    //     };

    //     const fetchInc = async () => {
    //         try {
    //             const response = await fetch(`/income_statements/${company.cik}`);
    //             if (response.ok) {
    //                 const data = await response.json();
    //                 setIncApi(data)
    //             } else {
    //                 setIncApi([])
    //                 console.error('Failed to fetch income staements:', response.status);
    //             }
    //         } catch (error) {
    //             console.error('Error fetching income staements:', error);
    //         }
    //     };

    //     const fetchCf = async () => {
    //         try {
    //             const response = await fetch(`/cf_statements/${company.cik}`);
    //             if (response.ok) {
    //                 const data = await response.json();
    //                 setCfApi(data)
    //             } else {
    //                 setCfApi([])
    //                 console.error('Failed to fetch cashflow staements:', response.status);
    //             }
    //         } catch (error) {
    //             console.error('Error fetching cashflow staements:', error);
    //         }
    //     };
    //     // FUNCTIONS END///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        
    //     if (company){
    //         fetchBs()
    //         fetchInc()
    //         fetchCf()
    //     }
        
    // },[company])

//// 1.) Create data and labels for bar and other charts ////////////////////////////////////////////////////////////////////////////////////////////////
    if(company){
        assetsData = company.balance_sheets.map(bs => bs.total_assets)
        assetsLabels = company.balance_sheets.map(bs => bs.end)
        liabilitiesData = company.balance_sheets.map(bs => bs.total_liabilities)
        stockholdersData = company.balance_sheets.map(bs => bs.total_stockholders_equity)
        primaryLabels = assetsLabels

        revenueData = company.income_statements.map(inc => inc.total_revenue)
        revenueLabels = company.income_statements.map(inc => inc.end)

        opCfData = company.cash_flows.map(cf => cf.opr_cf)
        opCfLabels = company.cash_flows.map(cf => cf.end)

        invCfData = company.cash_flows.map(cf => cf.inv_cf)
        invCfLabels = company.cash_flows.map(cf => cf.end)

        finCfData = company.cash_flows.map(cf => cf.fin_cf)
        finCfLabels = company.cash_flows.map(cf => cf.end)

        netCfData = company.cash_flows.map(cf => cf.net_cf)
        netCfLabels = company.cash_flows.map(cf => cf.end)

        cashData = company.balance_sheets.map(bs => bs.cash_and_equiv)

        goodwillData = company.balance_sheets.map(bs => bs.goodwill)
        goodwillLabels = company.balance_sheets.map(bs => bs.end)

        netIncomeData = company.income_statements.map(inc => inc.net_income)
        netIncomeLabels = company.income_statements.map(inc => inc.end)
    }

    function formatNumber(num) {
        if (typeof num !== 'number' || isNaN(num)) {
            return 0;
        }
        if (Math.abs(num) >= 1000000000000) {
            return (num / 1000000000000).toFixed(3) + ' T';
        } else if (Math.abs(num) >= 1000000000) {
            return (num / 1000000000).toFixed(3) + ' B';
        } else if (Math.abs(num) >= 1000000) {
            return (num / 1000000).toFixed(3) + ' M';
        } else if (Math.abs(num) >= 1000) {
            return (num / 1000).toFixed(3) + ' K';
        } else {
            return num.toFixed(0);
        }
    }
    
    // define data for LINE graphs
    function lineData(labels, data, data2, data3, data4, data5){
        const dataObj = {
            labels: labels,
            datasets: [{
                label: 'Assets',
                data: data,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            },
            {
                label: 'Liabilities',
                data: data2,
                fill: false,
                borderColor: 'rgb(255, 0, 0)',
                tension: 0.1
            },
            {
                label: `Stockholders' Equity`,
                data: data3,
                fill: false,
                borderColor: 'rgb(0, 0, 0)',
                tension: 0.1
            },
            {
                label: `Cash and Equivalents`,
                data: data5,
                fill: false,
                borderColor: 'rgb(0, 128, 0)',
                tension: 0.1
            },
            {
                label: `Goodwill`,
                data: data4,
                fill: false,
                borderColor: 'rgb(255, 255, 0)',
                tension: 0.1
            },
            
            ]
        };
        return dataObj
    }

    function revData(labels,data, data2){
        const dataObj = {
            labels: labels,
            datasets: [
            {
                label: 'Net Income',
                data: data2,
                fill: false,
                borderColor: 'rgb(255, 0, 0)',
                tension: 0.1
            }, 
            {
                label: 'Revenue',
                data: data,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            },
            
            ]
        };
        return dataObj
    }

    function cfData(labels, data, data2, data3,data4){
        const dataObj = {
            labels: labels,
            datasets: [{
                label: 'Operating Cashflows',
                data: data,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            },
            {
                label: 'Investing Cashflows',
                data: data2,
                fill: false,
                borderColor: 'rgb(0, 0, 255)',
                tension: 0.1
            },
            {
                label: `Financing Cashflows`,
                data: data3,
                fill: false,
                borderColor: 'rgb(255, 0, 0)',
                tension: 0.1
            },
            {
                label: `Net Cashflows`,
                data: data4,
                fill: false,
                borderColor: 'rgb(255, 100, 100)',
                tension: 0.1
            }]
        }
        
        
        return dataObj
    }

    // define options for LINE graphs
    const options = {
        responsive: true,
        elements: {
            line: {
                borderWidth: 5,
                capBezierPoints: false,
                lineJoin: 'round',

            },
            point:{
                // pointStyle: false,
                pointRadius: 2,
            },
        },

        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const label1 = context.dataset.label + ': ' + company.income_statements[0].currency + ' ' + formatNumber(context.parsed.y);
                       
                        return label1;
              }
            }
          },
          
        },
        scales:{
            y:{
            },
        },
    }
    
    // Define data for BAR graphs
    function barData(labels, data, dataSetLabel, backgroundColor = 'rgba(75, 192, 192, 0.2)', borderColor = 'rgba(75, 192, 192, 1)', borderWidth = 1){
        const dataObj = {
            labels: labels, // X-axis labels
            datasets: [
                {
                    label: dataSetLabel, // Label for the dataset
                    data: data, // Y-axis data
                    backgroundColor: backgroundColor, // Bar color
                    borderColor: borderColor, // Bar border color
                    borderWidth: borderWidth, // Bar border width
                },
            ],
        };
        return dataObj
    }

    // Define options for BAR graphs
    function barOptions(header){
        const optionsObj = {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top', // Position of the legend
                },
                title: {
                    display: true,
                    text: header, // Title of the chart
                },
            },
        };
        return optionsObj
    }

    // {/* <Bar data={barData(cashLabels, cashData, "Cash")} options={barOptions("Cash History")} /> */}
    // {/* <p>${company && cashPath[cashPath.length - 1].val.toLocaleString('en-US')} Cash & Equivialents as of: {company && cashPath[cashPath.length - 1].end}</p> */}

//// 2.) Render component in JSX ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    // ## BAR DATA TEMPLATE ##: function barData(labels, data, dataSetLabel, backgroundColor = 'rgba(75, 192, 192, 0.2)', borderColor = 'rgba(75, 192, 192, 1)', borderWidth = 1)
    return(
        <>  <div id ="stats">
                <p>CIK ID: {company.cik}</p>
                <p>Latest financial statements as of: {company && assetsLabels[assetsLabels.length - 1]} </p>
                <p className='figures'>Assets: {company && company.income_statements.length > 0 ? company.income_statements[0].currency : ''} {company && assetsData.length > 0 ? formatNumber(assetsData[assetsData.length - 1]) : ''}</p>
                <p className='figures'>Liabilities: {company && company.income_statements.length > 0 ? company.income_statements[0].currency : ''} {company && liabilitiesData.length > 0 ? formatNumber(liabilitiesData[liabilitiesData.length - 1]) : ''}</p>
                <p className='figures'>Stockholders Equity: {company && company.income_statements.length > 0 ? company.income_statements[0].currency : ''} {company && stockholdersData.length > 0 ? formatNumber(stockholdersData[stockholdersData.length - 1]) : ''}</p>
                <p className='figures'>Last reported cash balance: {company && company.income_statements.length > 0 ? company.income_statements[0].currency : ''} {company && cashData.length > 0 ? formatNumber(cashData[cashData.length - 1]) : ''}</p>
            </div>
            <div id ="cash-graph-div">
                <div className = "fin-graph">
                    <Line data={lineData(primaryLabels, assetsData, liabilitiesData, stockholdersData, goodwillData, cashData)} options={options}/>
                </div>
                <div className = "fin-graph">
                    <Line data={revData(netIncomeLabels, revenueData, netIncomeData)} options={options}/>
                </div>
                <div className = "fin-graph">
                    <Line data={cfData(opCfLabels, opCfData, invCfData, finCfData, netCfData, )} options={options}/>
                </div>
            </div>  
        </>
    )
}