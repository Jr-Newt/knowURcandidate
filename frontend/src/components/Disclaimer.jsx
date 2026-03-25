export default function Disclaimer() {
  return (
    <div className="bg-neutral-100 border border-neutral-200 rounded-lg px-4 py-3 flex items-start gap-2.5">
      <svg className="w-4 h-4 text-neutral-400 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p className="text-xs text-neutral-500 leading-relaxed">
        <span className="font-medium text-neutral-600">Disclaimer:</span> Ranking is based on user-selected preferences and does not represent any official, editorial, or political position. Data sourced from Election Commission affidavits.
      </p>
    </div>
  );
}
