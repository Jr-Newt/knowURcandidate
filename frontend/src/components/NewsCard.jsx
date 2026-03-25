export default function NewsCard({ article }) {
  return (
    <a
      href={article.url}
      target="_blank"
      rel="noopener noreferrer"
      className="block bg-white border border-neutral-200 rounded-xl p-4 hover:border-neutral-300 transition-colors"
    >
      <h3 className="text-sm font-medium text-neutral-800 mb-1 line-clamp-2">{article.title}</h3>
      {article.summary && (
        <p className="text-xs text-neutral-500 mb-2 line-clamp-2">{article.summary}</p>
      )}
      <div className="flex items-center gap-2 text-[10px] text-neutral-400">
        {article.source && (
          <span className="font-medium text-neutral-500">{article.source}</span>
        )}
        {article.source && article.published_date && <span>·</span>}
        {article.published_date && (
          <span>{new Date(article.published_date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}</span>
        )}
        <span className="ml-auto text-accent-500">↗</span>
      </div>
    </a>
  );
}
