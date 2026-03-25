import { Link } from 'react-router-dom';

function formatCurrency(amount) {
  if (!amount) return '₹0';
  if (amount >= 10000000) return `₹${(amount / 10000000).toFixed(1)} Cr`;
  if (amount >= 100000) return `₹${(amount / 100000).toFixed(1)} L`;
  return `₹${amount.toLocaleString('en-IN')}`;
}

export default function CandidateCard({ candidate, isSelected, onToggleCompare }) {
  const c = candidate;

  return (
    <div className={`bg-white border rounded-xl p-5 transition-all hover:border-neutral-300 ${
      isSelected ? 'border-accent-300 ring-1 ring-accent-100' : 'border-neutral-200'
    }`}>
      <div className="flex items-start gap-3 mb-3">
        {/* Avatar */}
        <div className="w-10 h-10 rounded-full bg-accent-100 text-accent-700 flex items-center justify-center text-sm font-bold shrink-0">
          {c.name.split(' ').map(n => n[0]).join('').slice(0, 2)}
        </div>
        <div className="flex-1 min-w-0">
          <Link
            to={`/candidate/${c.id}`}
            className="font-medium text-neutral-900 text-sm hover:text-accent-600 transition-colors block truncate"
          >
            {c.name}
          </Link>
          <div className="flex items-center gap-1.5 mt-0.5">
            <span className="text-xs px-1.5 py-0.5 rounded bg-neutral-100 text-neutral-600 font-medium">
              {c.party}
            </span>
            <span className="text-[10px] text-neutral-400 truncate">
              {c.constituency_name}
            </span>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 gap-2 text-xs mb-3">
        <div className="bg-neutral-50 rounded-lg px-2.5 py-1.5">
          <span className="text-neutral-400 block text-[10px]">Education</span>
          <span className="text-neutral-700 font-medium">{c.education || 'N/A'}</span>
        </div>
        <div className="bg-neutral-50 rounded-lg px-2.5 py-1.5">
          <span className="text-neutral-400 block text-[10px]">Assets</span>
          <span className="text-neutral-700 font-medium">{formatCurrency(c.assets)}</span>
        </div>
        <div className={`rounded-lg px-2.5 py-1.5 ${c.criminal_cases > 0 ? 'bg-danger-50' : 'bg-success-50'}`}>
          <span className="text-neutral-400 block text-[10px]">Criminal Cases</span>
          <span className={`font-medium ${c.criminal_cases > 0 ? 'text-danger-600' : 'text-success-600'}`}>
            {c.criminal_cases}
            {c.serious_cases > 0 && <span className="text-danger-500"> ({c.serious_cases} serious)</span>}
          </span>
        </div>
        <div className="bg-neutral-50 rounded-lg px-2.5 py-1.5">
          <span className="text-neutral-400 block text-[10px]">Age</span>
          <span className="text-neutral-700 font-medium">{c.age || 'N/A'}</span>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-2">
        <Link
          to={`/candidate/${c.id}`}
          className="flex-1 text-center py-1.5 text-xs font-medium text-accent-600 border border-accent-200 rounded-lg hover:bg-accent-50 transition-all"
        >
          View Profile
        </Link>
        <button
          onClick={onToggleCompare}
          className={`px-3 py-1.5 text-xs font-medium rounded-lg border transition-all ${
            isSelected
              ? 'bg-accent-600 text-white border-accent-600'
              : 'text-neutral-500 border-neutral-200 hover:border-neutral-300'
          }`}
        >
          {isSelected ? '✓' : '+'}
        </button>
      </div>
    </div>
  );
}
