const path = require("path");
require('react-scripts/config/env');
module.exports = {
    webpack: {
        alias: {
            "@": path.resolve(__dirname, "src/"),
        },
    },
};
