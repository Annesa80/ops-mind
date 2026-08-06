function SourceList({sources}) {

    return (
        <ul>
            {sources.map(source=>(
                <li key={source}>
                    📄 {source}
                </li>
            ))}
        </ul>
    );
}

export default SourceList;