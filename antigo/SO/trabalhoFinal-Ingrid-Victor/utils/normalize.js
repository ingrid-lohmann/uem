const regex = /\s/g;

const normalize = (str) => {
    return str.toLowerCase().replace(regex, '');
}

module.exports = normalize;