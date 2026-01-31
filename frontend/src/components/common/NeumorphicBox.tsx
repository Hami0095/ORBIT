import React from 'react';

interface NeumorphicBoxProps {
    children: React.ReactNode;
    className?: string;
    variant?: 'flat' | 'inset' | 'pressed' | 'card';
}

const NeumorphicBox: React.FC<NeumorphicBoxProps> = ({
    children,
    className = '',
    variant = 'flat'
}) => {
    const variantClasses = {
        flat: 'neumorphic-flat',
        inset: 'neumorphic-inset',
        pressed: 'neumorphic-pressed',
        card: 'neumorphic-card',
    };

    return (
        <div className={`${variantClasses[variant]} ${className}`}>
            {children}
        </div>
    );
};

export default NeumorphicBox;
