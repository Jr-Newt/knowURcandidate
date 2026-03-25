export default function RedFlag({ type, title, subtitle }) {
  const config = {
    criminal: {
      bg: 'bg-danger-50',
      border: 'border-danger-200',
      icon: (
        <svg className="w-4 h-4 text-danger-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
      ),
      label: 'Criminal Record',
    },
    wealth: {
      bg: 'bg-warning-50',
      border: 'border-yellow-200',
      icon: (
        <svg className="w-4 h-4 text-warning-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      label: 'Wealth Alert',
    },
  };

  const c = config[type] || config.criminal;

  return (
    <div className={`${c.bg} border ${c.border} rounded-lg p-3 flex items-start gap-2.5`}>
      <div className="shrink-0 mt-0.5">{c.icon}</div>
      <div>
        <p className="text-sm font-medium text-neutral-800">{title}</p>
        {subtitle && <p className="text-xs text-neutral-500 mt-0.5">{subtitle}</p>}
      </div>
    </div>
  );
}
