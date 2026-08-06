function AnswerBox({ answer }) {

    if (!answer) return null;

    return (
        <div className="mt-8">

            <h2 className="text-2xl font-bold mb-3">
                Answer
            </h2>

            <div className="bg-gray-100 rounded-lg p-5 whitespace-pre-wrap">
                {answer}
            </div>

        </div>
    );
}

export default AnswerBox;