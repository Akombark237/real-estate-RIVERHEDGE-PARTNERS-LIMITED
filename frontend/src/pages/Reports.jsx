import { useState, useEffect } from 'react';
import axios from 'axios';
import showToast, { getErrorMessage } from '../utils/toast';

const Reports = () => {
  const [reportType, setReportType] = useState('transactions');
  const [dateRange, setDateRange] = useState({
    startDate: new Date(new Date().setMonth(new Date().getMonth() - 1)).toISOString().split('T')[0],
    endDate: new Date().toISOString().split('T')[0]
  });
  const [loading, setLoading] = useState(false);
  const [reportData, setReportData] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [properties, setProperties] = useState([]);
  const [materials, setMaterials] = useState([]);

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      const [transactionsRes, propertiesRes, materialsRes] = await Promise.all([
        axios.get('/api/properties/transactions/'),
        axios.get('/api/properties/'),
        axios.get('/api/materials/')
      ]);

      setTransactions(transactionsRes.data.results || transactionsRes.data || []);
      setProperties(propertiesRes.data.results || propertiesRes.data || []);
      setMaterials(materialsRes.data.results || materialsRes.data || []);
    } catch (error) {
      console.error('Failed to fetch data:', error);
      showToast.error(getErrorMessage(error));
    }
  };

  const generateReport = () => {
    setLoading(true);
    
    try {
      let data = null;
      
      switch (reportType) {
        case 'transactions':
          data = generateTransactionReport();
          break;
        case 'commission':
          data = generateCommissionReport();
          break;
        case 'properties':
          data = generatePropertyReport();
          break;
        case 'materials':
          data = generateMaterialReport();
          break;
        default:
          data = null;
      }
      
      setReportData(data);
      showToast.success('Report generated successfully!');
    } catch (error) {
      console.error('Error generating report:', error);
      showToast.error('Failed to generate report');
    } finally {
      setLoading(false);
    }
  };

  const generateTransactionReport = () => {
    const filtered = transactions.filter(t => {
      if (!t.transaction_date) return false;
      const date = new Date(t.transaction_date);
      return date >= new Date(dateRange.startDate) && date <= new Date(dateRange.endDate);
    });

    const totalRevenue = filtered.reduce((sum, t) => sum + parseFloat(t.sale_price || 0), 0);
    const totalCommission = filtered.reduce((sum, t) => sum + parseFloat(t.commission_amount || 0), 0);
    const completedCount = filtered.filter(t => t.status === 'completed').length;

    return {
      title: 'Transaction Report',
      summary: {
        'Total Transactions': filtered.length,
        'Completed Transactions': completedCount,
        'Total Revenue': `$${totalRevenue.toLocaleString()}`,
        'Total Commission': `$${totalCommission.toLocaleString()}`,
        'Average Sale Price': filtered.length > 0 ? `$${(totalRevenue / filtered.length).toLocaleString()}` : '$0',
        'Average Commission': filtered.length > 0 ? `$${(totalCommission / filtered.length).toLocaleString()}` : '$0'
      },
      details: filtered,
      type: 'transactions'
    };
  };

  const generateCommissionReport = () => {
    const filtered = transactions.filter(t => {
      if (!t.transaction_date) return false;
      const date = new Date(t.transaction_date);
      return date >= new Date(dateRange.startDate) && date <= new Date(dateRange.endDate);
    });

    const byAgent = {};
    filtered.forEach(t => {
      const agentName = t.agent?.full_name || t.agent?.email || 'Unassigned';
      if (!byAgent[agentName]) {
        byAgent[agentName] = {
          count: 0,
          totalCommission: 0,
          totalSales: 0
        };
      }
      byAgent[agentName].count += 1;
      byAgent[agentName].totalCommission += parseFloat(t.commission_amount || 0);
      byAgent[agentName].totalSales += parseFloat(t.sale_price || 0);
    });

    const totalCommission = filtered.reduce((sum, t) => sum + parseFloat(t.commission_amount || 0), 0);

    return {
      title: 'Commission Report',
      summary: {
        'Total Commission Earned': `$${totalCommission.toLocaleString()}`,
        'Number of Agents': Object.keys(byAgent).length,
        'Total Transactions': filtered.length,
        'Average Commission per Transaction': filtered.length > 0 ? `$${(totalCommission / filtered.length).toLocaleString()}` : '$0'
      },
      byAgent: byAgent,
      details: filtered,
      type: 'commission'
    };
  };

  const generatePropertyReport = () => {
    const statusCounts = {
      available: 0,
      pending: 0,
      sold: 0,
      rented: 0,
      off_market: 0
    };

    const typeCounts = {};
    let totalValue = 0;

    properties.forEach(p => {
      if (statusCounts.hasOwnProperty(p.status)) {
        statusCounts[p.status]++;
      }
      
      if (!typeCounts[p.property_type]) {
        typeCounts[p.property_type] = 0;
      }
      typeCounts[p.property_type]++;
      
      totalValue += parseFloat(p.price || 0);
    });

    return {
      title: 'Property Report',
      summary: {
        'Total Properties': properties.length,
        'Available': statusCounts.available,
        'Pending': statusCounts.pending,
        'Sold': statusCounts.sold,
        'Rented': statusCounts.rented,
        'Off Market': statusCounts.off_market,
        'Total Portfolio Value': `$${totalValue.toLocaleString()}`,
        'Average Property Value': properties.length > 0 ? `$${(totalValue / properties.length).toLocaleString()}` : '$0'
      },
      byType: typeCounts,
      byStatus: statusCounts,
      details: properties,
      type: 'properties'
    };
  };

  const generateMaterialReport = () => {
    const byCategoryCount = {};
    const byCategoryValue = {};

    materials.forEach(m => {
      const category = m.category || 'Uncategorized';
      if (!byCategoryCount[category]) {
        byCategoryCount[category] = 0;
        byCategoryValue[category] = 0;
      }
      byCategoryCount[category]++;
      byCategoryValue[category] += parseFloat(m.current_price || 0);
    });

    return {
      title: 'Material Inventory Report',
      summary: {
        'Total Materials': materials.length,
        'Total Categories': Object.keys(byCategoryCount).length,
        'Total Inventory Value': `$${Object.values(byCategoryValue).reduce((a, b) => a + b, 0).toLocaleString()}`
      },
      byCategory: byCategoryCount,
      details: materials,
      type: 'materials'
    };
  };

  const exportToCSV = () => {
    if (!reportData) {
      showToast.error('Please generate a report first');
      return;
    }

    let csvContent = '';
    
    // Add title
    csvContent += `${reportData.title}\n`;
    csvContent += `Generated: ${new Date().toLocaleString()}\n`;
    csvContent += `Date Range: ${dateRange.startDate} to ${dateRange.endDate}\n\n`;
    
    // Add summary
    csvContent += 'SUMMARY\n';
    Object.entries(reportData.summary).forEach(([key, value]) => {
      csvContent += `${key},${value}\n`;
    });
    csvContent += '\n';
    
    // Add details based on report type
    if (reportData.type === 'transactions') {
      csvContent += 'TRANSACTION DETAILS\n';
      csvContent += 'Property,Sale Price,Commission,Status,Date\n';
      reportData.details.forEach(t => {
        csvContent += `"${t.property?.title || 'N/A'}",${t.sale_price},${t.commission_amount},${t.status},${t.transaction_date || 'N/A'}\n`;
      });
    } else if (reportData.type === 'commission') {
      csvContent += 'COMMISSION BY AGENT\n';
      csvContent += 'Agent,Transactions,Total Sales,Total Commission\n';
      Object.entries(reportData.byAgent).forEach(([agent, data]) => {
        csvContent += `"${agent}",${data.count},$${data.totalSales.toLocaleString()},$${data.totalCommission.toLocaleString()}\n`;
      });
    } else if (reportData.type === 'properties') {
      csvContent += 'PROPERTY DETAILS\n';
      csvContent += 'Title,Type,Status,Price,Location\n';
      reportData.details.forEach(p => {
        csvContent += `"${p.title}",${p.property_type},${p.status},$${p.price},"${p.city}, ${p.state}"\n`;
      });
    } else if (reportData.type === 'materials') {
      csvContent += 'MATERIAL DETAILS\n';
      csvContent += 'Name,Category,Unit,Current Price,Supplier\n';
      reportData.details.forEach(m => {
        csvContent += `"${m.name}",${m.category},${m.unit},$${m.current_price || 0},"${m.supplier?.name || 'N/A'}"\n`;
      });
    }

    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `${reportType}_report_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showToast.success('Report exported to CSV!');
  };

  const printReport = () => {
    if (!reportData) {
      showToast.error('Please generate a report first');
      return;
    }
    window.print();
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  return (
    <div className="px-4 py-6 sm:px-0">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-indigo-700 rounded-xl shadow-lg p-8 mb-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 opacity-10">
          <svg className="h-48 w-48" fill="currentColor" viewBox="0 0 24 24">
            <path d="M9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4zm2.5 2.1h-15V5h15v14.1zm0-16.1h-15c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h15c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"/>
          </svg>
        </div>
        <div className="relative z-10">
          <h1 className="text-4xl font-bold text-white mb-2">Reports & Analytics</h1>
          <p className="text-indigo-100 text-lg">Generate comprehensive business reports</p>
        </div>
      </div>

      {/* Report Configuration */}
      <div className="bg-white shadow-xl rounded-2xl p-6 mb-6 border border-gray-100">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Report Configuration</h2>
        
        <div className="grid md:grid-cols-3 gap-6">
          {/* Report Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Report Type
            </label>
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-lg"
            >
              <option value="transactions">Transaction Report</option>
              <option value="commission">Commission Report</option>
              <option value="properties">Property Report</option>
              <option value="materials">Material Inventory Report</option>
            </select>
          </div>

          {/* Start Date */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Start Date
            </label>
            <input
              type="date"
              value={dateRange.startDate}
              onChange={(e) => setDateRange(prev => ({ ...prev, startDate: e.target.value }))}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>

          {/* End Date */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              End Date
            </label>
            <input
              type="date"
              value={dateRange.endDate}
              onChange={(e) => setDateRange(prev => ({ ...prev, endDate: e.target.value }))}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-6 flex flex-wrap gap-3">
          <button
            onClick={generateReport}
            disabled={loading}
            className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-indigo-700 text-white rounded-lg hover:from-indigo-700 hover:to-indigo-800 transition-all font-semibold disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating...
              </>
            ) : (
              <>
                <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Generate Report
              </>
            )}
          </button>

          {reportData && (
            <>
              <button
                onClick={exportToCSV}
                className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-semibold flex items-center"
              >
                <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Export CSV
              </button>

              <button
                onClick={printReport}
                className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors font-semibold flex items-center"
              >
                <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                </svg>
                Print
              </button>
            </>
          )}
        </div>
      </div>

      {/* Report Display */}
      {reportData && (
        <div className="bg-white shadow-xl rounded-2xl p-8 border border-gray-100 print:shadow-none">
          {/* Report Header */}
          <div className="border-b border-gray-200 pb-6 mb-6">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">{reportData.title}</h2>
            <p className="text-gray-600">
              Generated: {new Date().toLocaleString()} | 
              Period: {dateRange.startDate} to {dateRange.endDate}
            </p>
          </div>

          {/* Summary Section */}
          <div className="mb-8">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Summary</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(reportData.summary).map(([key, value]) => (
                <div key={key} className="bg-gradient-to-br from-indigo-50 to-blue-50 p-4 rounded-lg border border-indigo-100">
                  <div className="text-sm text-gray-600 mb-1">{key}</div>
                  <div className="text-2xl font-bold text-gray-900">{value}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Commission by Agent (for commission reports) */}
          {reportData.type === 'commission' && reportData.byAgent && (
            <div className="mb-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Commission by Agent</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Agent</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Transactions</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total Sales</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total Commission</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {Object.entries(reportData.byAgent).map(([agent, data]) => (
                      <tr key={agent}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{agent}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{data.count}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatPrice(data.totalSales)}</td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-green-600">{formatPrice(data.totalCommission)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Details Section */}
          <div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Detailed Data</h3>
            <p className="text-gray-600 mb-4">
              Total Records: {reportData.details.length}
            </p>
            <div className="text-sm text-gray-500">
              Export to CSV or print for full details
            </div>
          </div>
        </div>
      )}

      {/* Empty State */}
      {!reportData && !loading && (
        <div className="bg-white shadow-xl rounded-2xl p-12 text-center border border-gray-100">
          <div className="flex flex-col items-center">
            <div className="bg-indigo-100 p-4 rounded-full mb-4">
              <svg className="h-16 w-16 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <p className="text-gray-500 text-lg font-medium">No report generated yet</p>
            <p className="text-gray-400 text-sm mt-1">Select a report type and date range, then click "Generate Report"</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Reports;

