import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

export default function Chat() {
    const { chat_id } = useParams<{ chat_id: string }>();
    const { t } = useTranslation();

    return (
        <main>
            <h1>{t('greeting')}</h1>
            <p>chat with id {chat_id} page placegolder text</p>
        </main>
    );
}