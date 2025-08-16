//Unused for now

export const Activity = {
    Online: "online",
    Offline: "offline",
    Invisible: "invisible",
} as const;

export type Activity = (typeof Activity)[keyof typeof Activity];

type Props = {
    activity: Activity;
};

export default function ActivityIndicator({activity}: Props) {
    const getColor = (activity: Activity): string => {
        switch (activity) {
            case Activity.Online:
                return "bg-green-500";
            case Activity.Offline:
                return "bg-red-500";
            case Activity.Invisible:
                return "bg-gray-400";
            default:
                return "bg-gray-400";
        }
    };

    return (
        <div className={`w-3 h-3 rounded-full ${getColor(activity)}`} />
    );
}
