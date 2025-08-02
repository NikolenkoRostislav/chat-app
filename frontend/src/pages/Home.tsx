import { useTranslation } from 'react-i18next';

export default function Home() {
    const { t } = useTranslation(); 

    return (
        <main>
            <h1>{t('greeting')}</h1>
            <p>home page placegolder text</p>
        </main>
    );
}