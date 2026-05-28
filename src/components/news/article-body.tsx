import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/** Рендер Markdown-тела статьи в премиальной prose-типографике. */
export function ArticleBody({ content }: { content: string }) {
  return (
    <div className="article-body">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
    </div>
  );
}
