import { useTranslation } from 'react-i18next';
import RouteButton from '../components/RouteButton';

export default function Home() {
    const { t } = useTranslation(); 

    return (
        <main>
            <h1>{t('greeting')}</h1>
            <p>home page placegolder text</p>
            <RouteButton route="chat/12345">
                <p>{t('go_to_chat')}</p>
            </RouteButton>
            <RouteButton route="chat/67890">
                <p>{t('go_to_another_chat')}</p>
            </RouteButton>
        </main>
    );
}