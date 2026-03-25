import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { fetchCandidate } from '../api/client';

function formatCurrency(amount) {
  if (!amount) return '₹0';
  if (amount >= 10000000) return `₹${(amount / 10000000).toFixed(2)} Cr`;
  if (amount >= 100000) return `₹${(amount / 100000).toFixed(2)} L`;
  return `₹${amount.toLocaleString('en-IN')}`;
}

function CompareRow({ label, values, format = 'text', highlight = 'none' }) {
  const getHighlightClass = (val, allVals) => {
    if (highlight === 'none') return '';
    const nums = allVals.map(Number).filter((n) => !isNaN(n));
    if (nums.length < 2) return '';
    const best = highlight === 'high' ? Math.max(...nums) : Math.min(...nums);
    return Number(val) === best ? 'bg-success-50 text-success-700' : '';
  };

  const allRaw = values.map((v) => v);

  return (
    <tr className="border-b border-neutral-100 last:border-0">
      <td className="py-3 pr-4 text-xs font-medium text-neutral-500 whitespace-nowrap">{label}</td>
      {values.map((val, i) => (
        <td key={i} className={`py-3 px-3 text-sm text-neutral-800 text-center ${getHighlightClass(val, allRaw)}`}>
          {format === 'currency' ? formatCurrency(val) : format === 'percent' ? `${Math.round(val * 100)}%` : val ?? '—'}
        </td>
      ))}
    </tr>
  );
}

export default function ComparisonView() {
  const [searchParams] = useSearchParams();
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const ids = searchParams.get('ids');
    if (!ids) {
      setLoading(false);
      return;
    }
    const idList = ids.split(',').map(Number).filter(Boolean);
    Promise.all(idList.map(fetchCandidate))
      .then(setCandidates)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [searchParams]);

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="animate-pulse h-64 bg-neutral-100 rounded-xl"></div>
      </div>
    );
  }

  if (candidates.length < 2) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h1 className="text-xl font-semibold text-neutral-900 mb-2">Compare Candidates</h1>
        <p className="text-sm text-neutral-400 mb-4">Select at least 2 candidates from the candidate list to compare.</p>
        <Link to="/candidates" className="text-accent-600 text-sm hover:underline">
          ← Go to Candidate List
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-xl font-semibold text-neutral-900 mb-1">Compare Candidates</h1>
      <p className="text-sm text-neutral-500 mb-6">Side-by-side comparison of selected candidates</p>

      <div className="bg-white border border-neutral-200 rounded-xl overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-neutral-200">
              <th className="py-4 px-4 text-left text-xs font-medium text-neutral-400 w-32">Metric</th>
              {candidates.map((c) => (
                <th key={c.id} className="py-4 px-3 text-center">
                  <div className="flex flex-col items-center gap-1">
                    <div className="w-10 h-10 rounded-full bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-bold">
                      {c.name.split(' ').map(n => n[0]).join('').slice(0, 2)}
                    </div>
                    <Link to={`/candidate/${c.id}`} className="text-sm font-medium text-neutral-900 hover:text-accent-600 transition-colors">
                      {c.name}
                    </Link>
                    <span className="text-[10px] text-neutral-400">{c.party}</span>
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            <CompareRow label="Constituency" values={candidates.map(c => c.constituency_name)} />
            <CompareRow label="District" values={candidates.map(c => c.district_name)} />
            <CompareRow label="Age" values={candidates.map(c => c.age)} />
            <CompareRow label="Education" values={candidates.map(c => c.education)} />
            <CompareRow label="Profession" values={candidates.map(c => c.profession)} />
            <CompareRow label="Criminal Cases" values={candidates.map(c => c.criminal_cases)} highlight="low" />
            <CompareRow label="Serious Cases" values={candidates.map(c => c.serious_cases)} highlight="low" />
            <CompareRow label="Assets" values={candidates.map(c => c.assets)} format="currency" />
            <CompareRow label="Liabilities" values={candidates.map(c => c.liabilities)} format="currency" />
            <CompareRow label="Education Score" values={candidates.map(c => c.education_score)} format="percent" highlight="high" />
            <CompareRow label="Criminal Score" values={candidates.map(c => c.criminal_score)} format="percent" highlight="high" />
            <CompareRow label="Experience Score" values={candidates.map(c => c.experience_score)} format="percent" highlight="high" />
            <CompareRow label="Asset Score" values={candidates.map(c => c.asset_score)} format="percent" highlight="high" />
          </tbody>
        </table>
      </div>

      <p className="text-[10px] text-neutral-400 mt-4 text-center">
        Green highlights indicate the best value in each row. Data sourced from official election affidavits.
      </p>
    </div>
  );
}
